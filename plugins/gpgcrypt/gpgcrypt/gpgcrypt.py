# -*- coding: utf-8 -*-

#  gpgcrypt.py - Open and save GPG-encrypted files.
#
#  Copyright (C) 2026 MATE Developers
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110-1301, USA.

from gi.repository import GLib, GObject, Gio, Gtk, Pluma
import logging
import os
import shutil
import subprocess
import tempfile
import threading

_logger = logging.getLogger("GpgCryptPlugin")

GPG_EXTENSIONS = ('.gpg', '.pgp')


def _is_gpg_file(path):
    if path is None:
        return False
    return path.lower().endswith(GPG_EXTENSIONS)


def _decrypt_file(filepath):
    """Decrypt a GPG file using the gpg command.

    Returns a dict with keys: plaintext (bytes), returncode (int),
    stderr (str), method (str), recipients (list).
    """
    status_read, status_write = os.pipe()
    try:
        proc = subprocess.Popen(
            ['gpg', '--decrypt', '--status-fd', str(status_write), '--', filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            pass_fds=(status_write,),
        )
        os.close(status_write)
        status_write = -1
        stdout, stderr = proc.communicate()
        status_output = b''
        # Read all remaining status output after the subprocess exits
        while True:
            chunk = os.read(status_read, 65536)
            if not chunk:
                break
            status_output += chunk
    finally:
        if status_write != -1:
            os.close(status_write)
        os.close(status_read)

    status_text = status_output.decode('utf-8', errors='replace')
    recipients = []
    # Parse ENC_TO lines to detect asymmetric encryption and extract
    # recipient key IDs for re-encryption on save. If no ENC_TO lines
    # are present, the file was encrypted symmetrically (i.e. using
    # a password instead of a key).
    for line in status_text.splitlines():
        if line.startswith('[GNUPG:] ENC_TO '):
            parts = line.split()
            if len(parts) >= 3:
                recipients.append(parts[2])

    method = 'asymmetric' if recipients else 'symmetric'

    return {
        'plaintext': stdout,
        'returncode': proc.returncode,
        'stderr': stderr.decode('utf-8', errors='replace'),
        'method': method,
        'recipients': recipients,
    }


def _encrypt_content(plaintext_bytes, gpg_info, output_path):
    """Encrypt content and write to output_path.

    Returns (returncode, stderr_text).
    """
    cmd = ['gpg', '--yes']
    if gpg_info['method'] == 'symmetric':
        cmd.append('--symmetric')
    else:
        cmd.extend(['--batch', '--encrypt'])
        for recipient in gpg_info['recipients']:
            cmd.extend(['--recipient', recipient])
    cmd.extend(['--output', output_path])

    proc = subprocess.run(
        cmd,
        input=plaintext_bytes,
        capture_output=True,
    )
    return proc.returncode, proc.stderr.decode('utf-8', errors='replace')


def _show_error(window, title, message):
    dialog = Gtk.MessageDialog(
        transient_for=window,
        modal=True,
        message_type=Gtk.MessageType.ERROR,
        buttons=Gtk.ButtonsType.OK,
        text=title,
    )
    dialog.format_secondary_text(message)
    dialog.run()
    dialog.destroy()


class GpgCryptWindowActivatable(GObject.Object, Pluma.WindowActivatable):
    __gtype_name__ = "GpgCryptWindowActivatable"

    window = GObject.Property(type=Pluma.Window)

    def __init__(self):
        GObject.Object.__init__(self)
        self._handler_ids = {}

    def do_activate(self):
        if not shutil.which('gpg'):
            _logger.warning("gpg not found in PATH; GPG Encryption plugin disabled")
            return

        # Watch for new and removed tabs to attach/detach document signal
        # handlers. Also attach handlers to any tabs already open at the
        # time the plugin is activated (e.g. files passed on command line).
        self._handler_ids['tab-added'] = self.window.connect('tab-added', self._on_tab_added)
        self._handler_ids['tab-removed'] = self.window.connect('tab-removed', self._on_tab_removed)

        for view in self.window.get_views():
            self._attach_doc_handlers(view.get_buffer())

    def do_deactivate(self):
        for signal_name, handler_id in self._handler_ids.items():
            self.window.disconnect(handler_id)
        self._handler_ids.clear()

        for view in self.window.get_views():
            self._detach_doc_handlers(view.get_buffer())

    def do_update_state(self):
        pass

    def _on_tab_added(self, window, tab):
        self._attach_doc_handlers(tab.get_document())

    def _on_tab_removed(self, window, tab):
        self._detach_doc_handlers(tab.get_document())

    def _attach_doc_handlers(self, doc):
        if hasattr(doc, '_gpgcrypt_handlers'):
            return
        loaded_id = doc.connect('loaded', self._on_document_loaded)
        save_id = doc.connect('save', self._on_document_save)
        saved_id = doc.connect('saved', self._on_document_saved)
        doc._gpgcrypt_handlers = [loaded_id, save_id, saved_id]

    def _detach_doc_handlers(self, doc):
        if not hasattr(doc, '_gpgcrypt_handlers'):
            return
        for handler_id in doc._gpgcrypt_handlers:
            doc.disconnect(handler_id)
        del doc._gpgcrypt_handlers
        if hasattr(doc, '_gpgcrypt_info'):
            del doc._gpgcrypt_info

    def _on_document_loaded(self, doc, error):
        location = doc.get_location()
        if location is None:
            return

        path = location.get_path()
        if not _is_gpg_file(path):
            return

        had_error = bool(error)

        # Run decryption in a background thread so the GTK main loop
        # stays alive for pin entry prompts.
        thread = threading.Thread(
            target=self._decrypt_thread,
            args=(path, had_error),
            daemon=True,
        )
        thread.start()

    def _decrypt_thread(self, path, had_error):
        """Run gpg decryption in a background thread."""
        result = _decrypt_file(path)
        # Schedule UI update on the main thread
        GLib.idle_add(self._on_decrypt_done, path, had_error, result)

    def _on_decrypt_done(self, path, had_error, result):
        """Handle decryption result on the main thread."""
        if result['returncode'] != 0:
            if not had_error:
                _show_error(
                    self.window,
                    "GPG Decryption Failed",
                    result['stderr'].strip() or "Unknown error decrypting file.",
                )
            return GLib.SOURCE_REMOVE

        gpg_info = {
            'method': result['method'],
            'recipients': result['recipients'],
        }

        if had_error:
            # Binary GPG file failed Pluma's encoding detection.
            # The tab is stuck in LOADING_ERROR state. Close it
            # and open a fresh one.
            self._replace_tab_with_decrypted(path, result['plaintext'], gpg_info)
        else:
            # Pluma managed to load the file as text (unlikely for .gpg/.pgp
            # but possible). Replace the buffer content in-place.
            doc = self._find_doc_by_path(path)
            if doc is None:
                return GLib.SOURCE_REMOVE
            plaintext = result['plaintext'].decode('utf-8', errors='replace')
            doc.begin_not_undoable_action()
            doc.delete(doc.get_start_iter(), doc.get_end_iter())
            doc.insert(doc.get_start_iter(), plaintext)
            doc.end_not_undoable_action()
            doc.set_modified(False)
            doc.place_cursor(doc.get_start_iter())
            doc._gpgcrypt_info = gpg_info

        return GLib.SOURCE_REMOVE

    def _find_doc_by_path(self, path):
        for doc in self.window.get_documents():
            loc = doc.get_location()
            if loc and loc.get_path() == path:
                return doc
        return None

    def _replace_tab_with_decrypted(self, original_path, plaintext_bytes, gpg_info):
        """Close the error tab and open a new clean tab with decrypted content."""
        # Close the broken tab
        doc = self._find_doc_by_path(original_path)
        if doc is not None:
            old_tab = Pluma.Tab.get_from_document(doc)
            if old_tab is not None:
                self.window.close_tab(old_tab)

        # Create a new empty tab
        new_tab = self.window.create_tab(True)
        new_doc = new_tab.get_document()

        # Populate the new tab with the decrypted content as a single
        # non-undoable action so the user can't undo back to ciphertext.
        plaintext = plaintext_bytes.decode('utf-8', errors='replace')
        new_doc.begin_not_undoable_action()
        new_doc.insert(new_doc.get_start_iter(), plaintext)
        new_doc.end_not_undoable_action()

        # Set the document location so saving goes back to the GPG file.
        # Pluma's internal mtime starts at 0 for a new document. Set the
        # file's mtime to match so the first save doesn't trigger a false
        # "externally modified" warning.
        new_doc.set_uri(Gio.file_new_for_path(original_path).get_uri())
        os.utime(original_path, (0, 0))
        new_doc.set_modified(False)
        new_doc.place_cursor(new_doc.get_start_iter())

        new_doc._gpgcrypt_info = gpg_info
        self._attach_doc_handlers(new_doc)

    def _on_document_save(self, doc, uri, encoding, flags):
        """Back up the encrypted file before Pluma overwrites it with
        plaintext. The backup is restored immediately in _on_document_saved
        so plaintext does not persist on disk during encryption."""
        location = doc.get_location()
        if location is None:
            return

        path = location.get_path()
        if not _is_gpg_file(path):
            return

        if not os.path.exists(path):
            return

        backup = path + '.gpgcrypt-backup'
        shutil.copy2(path, backup)
        doc._gpgcrypt_backup = backup

    def _on_document_saved(self, doc, error):
        if error:
            self._cleanup_backup(doc)
            return

        location = doc.get_location()
        if location is None:
            return

        path = location.get_path()
        if not _is_gpg_file(path):
            if hasattr(doc, '_gpgcrypt_info'):
                del doc._gpgcrypt_info
            self._cleanup_backup(doc)
            return

        if not hasattr(doc, '_gpgcrypt_info'):
            doc._gpgcrypt_info = {
                'method': 'symmetric',
                'recipients': [],
            }

        plaintext = doc.get_text(doc.get_start_iter(), doc.get_end_iter(), True)
        plaintext_bytes = plaintext.encode('utf-8')

        stat = os.stat(path)
        saved_mtime_ns = stat.st_mtime_ns
        saved_atime_ns = stat.st_atime_ns

        # Immediately restore the encrypted backup over the plaintext
        # that Pluma just wrote, so ciphertext is on disk while
        # encryption runs (which may block on pinentry for symmetric).
        # Preserve the mtime so Pluma doesn't detect an external change.
        backup = getattr(doc, '_gpgcrypt_backup', None)
        if backup and os.path.exists(backup):
            shutil.copy2(backup, path)
            os.utime(path, ns=(saved_atime_ns, saved_mtime_ns))
        if hasattr(doc, '_gpgcrypt_backup'):
            del doc._gpgcrypt_backup

        gpg_info = doc._gpgcrypt_info.copy()

        thread = threading.Thread(
            target=self._encrypt_thread,
            args=(path, plaintext_bytes, gpg_info, backup, saved_mtime_ns, saved_atime_ns),
            daemon=True,
        )
        thread.start()

    def _encrypt_thread(self, path, plaintext_bytes, gpg_info, backup_path, saved_mtime_ns, saved_atime_ns):
        """Run gpg encryption in a background thread."""
        fd, tmp_path = tempfile.mkstemp(
            dir=os.path.dirname(path),
            prefix='.gpgcrypt-',
        )
        os.close(fd)

        returncode, stderr = _encrypt_content(plaintext_bytes, gpg_info, tmp_path)

        GLib.idle_add(
            self._on_encrypt_done,
            path, tmp_path, backup_path,
            returncode, stderr,
            saved_mtime_ns, saved_atime_ns
        )

    def _on_encrypt_done(self, path, tmp_path, backup_path, returncode, stderr, saved_mtime_ns, saved_atime_ns):
        """Handle encryption result on the main thread."""
        if returncode != 0:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            self._cleanup_backup_file(backup_path)
            _show_error(
                self.window,
                "GPG Encryption Failed",
                stderr.strip() or "Unknown error encrypting file.",
            )
            return GLib.SOURCE_REMOVE

        os.replace(tmp_path, path)
        os.utime(path, ns=(saved_atime_ns, saved_mtime_ns))
        self._cleanup_backup_file(backup_path)
        return GLib.SOURCE_REMOVE

    @staticmethod
    def _cleanup_backup(doc):
        """Remove the backup file referenced by a document."""
        backup = getattr(doc, '_gpgcrypt_backup', None)
        if backup and os.path.exists(backup):
            os.unlink(backup)
            del doc._gpgcrypt_backup

    @staticmethod
    def _cleanup_backup_file(backup_path):
        """Remove a backup file by path."""
        if backup_path and os.path.exists(backup_path):
            os.unlink(backup_path)
