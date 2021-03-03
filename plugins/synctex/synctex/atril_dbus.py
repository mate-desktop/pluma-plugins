#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is part of the Pluma Synctex plugin.
#
# Copyright (C) 2010 Jose Aliste <jose.aliste@gmail.com>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public Licence as published by the Free Software
# Foundation; either version 2 of the Licence, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public Licence for more
# details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see https://www.gnu.org/licenses/.

import dbus, subprocess, time

RUNNING, CLOSED = range(2)

AT_DAEMON_PATH = "/org/mate/atril/Daemon"
AT_DAEMON_NAME = "org.mate.atril.Daemon"
AT_DAEMON_IFACE = "org.mate.atril.Daemon"

ATRIL_PATH = "/org/mate/atril/Atril"
ATRIL_IFACE = "org.mate.atril.Application"

AT_WINDOW_IFACE = "org.mate.atril.Window"


class AtrilWindowProxy:
    """A DBUS proxy for an Atril Window."""
    daemon = None
    bus = None

    def __init__(self, uri, spawn = False, logger = None):
        self._log = logger
        self.uri = uri
        self.spawn = spawn
        self.status = CLOSED
        self.source_handler = None
        self.dbus_name = ''
        self._handler = None
        try:
            if AtrilWindowProxy.bus is None:
                AtrilWindowProxy.bus = dbus.SessionBus()

            if AtrilWindowProxy.daemon is None:
                AtrilWindowProxy.daemon = AtrilWindowProxy.bus.get_object(AT_DAEMON_NAME,
                                                AT_DAEMON_PATH,
                                                follow_name_owner_changes=True)
            AtrilWindowProxy.bus.add_signal_receiver(self._on_doc_loaded, signal_name="DocumentLoaded",
                                                      dbus_interface = AT_WINDOW_IFACE,
                                                      sender_keyword='sender')
            self._get_dbus_name(False)

        except dbus.DBusException:
            if self._log:
                self._log.debug("Could not connect to the Atril Daemon")

    def _on_doc_loaded(self, uri, **keyargs):
        if uri == self.uri and self._handler is None:
            self.handle_find_document_reply(keyargs['sender'])

    def _get_dbus_name(self, spawn):
        AtrilWindowProxy.daemon.FindDocument(self.uri,spawn,
                     reply_handler=self.handle_find_document_reply,
                     error_handler=self.handle_find_document_error,
                     dbus_interface = AT_DAEMON_IFACE)

    def handle_find_document_error(self, error):
        if self._log:
            self._log.debug("FindDocument DBus call has failed")

    def handle_find_document_reply(self, atril_name):
        if self._handler is not None:
            handler = self._handler
        else:
            handler = self.handle_get_window_list_reply
        if atril_name != '':
            self.dbus_name = atril_name
            self.status = RUNNING
            self.atril = AtrilWindowProxy.bus.get_object(self.dbus_name, ATRIL_PATH)
            self.atril.GetWindowList(dbus_interface = ATRIL_IFACE,
                          reply_handler = handler,
                          error_handler = self.handle_get_window_list_error)

    def handle_get_window_list_error (self, e):
        if self._log:
            self._log.debug("GetWindowList DBus call has failed")

    def handle_get_window_list_reply (self, window_list):
        if len(window_list) > 0:
            window_obj = AtrilWindowProxy.bus.get_object(self.dbus_name, window_list[0])
            self.window = dbus.Interface(window_obj,AT_WINDOW_IFACE)
            self.window.connect_to_signal("Closed", self.on_window_close)
            self.window.connect_to_signal("SyncSource", self.on_sync_source)
        else:
            #That should never happen.
            if self._log:
                self._log.debug("GetWindowList returned empty list")


    def set_source_handler (self, source_handler):
        self.source_handler = source_handler

    def on_window_close(self):
        self.window = None
        self.status = CLOSED

    def on_sync_source(self, input_file, source_link, timestamp):
        if self.source_handler is not None:
            self.source_handler(input_file, source_link, timestamp)

    def SyncView(self, input_file, data, time):
        if self.status == CLOSED:
            if self.spawn:
                self._tmp_syncview = [input_file, data, time];
                self._handler = self._syncview_handler
                self._get_dbus_name(True)
        else:
            self.window.SyncView(input_file, data, time,  dbus_interface = "org.mate.atril.Window")

    def _syncview_handler(self, window_list):
        self.handle_get_window_list_reply(window_list)

        if self.status == CLOSED:
            return False
        self.window.SyncView(self._tmp_syncview[0],self._tmp_syncview[1], self._tmp_syncview[2], dbus_interface="org.mate.atril.Window")
        del self._tmp_syncview
        self._handler = None
        return True

## This file can be used as a script to support forward search and backward search in vim.
## It should be easy to adapt to other editors.
##  atril_dbus  pdf_file  line_source input_file
if __name__ == '__main__':
    import dbus.mainloop.glib, sys, os, logging
    from gi.repository import GObject

    def print_usage():
        print('''
The usage is atril_dbus output_file line_number input_file from the directory of output_file.
''')
        sys.exit(1)

    if len(sys.argv)!=4:
        print_usage()
    try:
        line_number = int(sys.argv[2])
    except ValueError:
        print_usage()

    output_file = sys.argv[1]
    input_file  = sys.argv[3]
    path_output  = os.getcwd() + '/' + output_file
    path_input   = os.getcwd() + '/' + input_file

    if not os.path.isfile(path_output):
        print_usage()

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    logger = logging.getLogger("atril_dbus")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch.setFormatter(formatter)

    logger.addHandler(ch)
    a = AtrilWindowProxy('file://' + path_output, True,logger=logger)

    def sync_view(ev_window, path_input, line_number):
        ev_window.SyncView (path_input, (line_number, 1),0)

    GObject.timeout_add(400, sync_view, a, path_input, line_number)
    loop = GObject.MainLoop()
    loop.run()
# ex:ts=4:et:
