# -*- coding: utf-8 -*-
#
# windowactivatable.py - Multi Edit
#
# Copyright (C) 2014 - Jesse van den Kieboom
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see https://www.gnu.org/licenses/.

from gi.repository import GLib, GObject, Gio, Gtk, Pluma

from .viewactivatable import MultiEditViewActivatable

try:
    import gettext
    gettext.bindtextdomain('pluma-plugins')
    gettext.textdomain('pluma-plugins')
    _ = gettext.gettext
except:
    _ = lambda s: s

ui_str = """
<ui>
  <menubar name="MenuBar">
    <menu name="EditMenu" action="Edit">
      <placeholder name="EditOps_5">
        <menuitem name="MultiEditMode" action="MultiEditModeAction"/>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""

class MultiEditWindowActivatable(GObject.Object, Pluma.WindowActivatable):
    __gtype_name__ = "MultiEditPlugin"

    window = GObject.Property(type=Pluma.Window)

    def do_activate(self):
        self._insert_menu()

        self.window.multiedit_window_activatable = self

    def do_deactivate(self):
        self._remove_menu()
        delattr(self.window, 'multiedit_window_activatable')

    def _insert_menu(self):
        manager = self.window.get_ui_manager()

        self._action_group = Gtk.ActionGroup("PlumaMultiEditPluginActions")
        self._action_group.add_toggle_actions([('MultiEditModeAction',
                                                None,
                                                _('Multi Edit Mode'),
                                                '<Ctrl><Shift>C',
                                                _('Start multi edit mode'),
                                                self.on_multi_edit_mode)])

        manager.insert_action_group(self._action_group)
        self._ui_id = manager.add_ui_from_string(ui_str)

    def _remove_menu(self):
        manager = self.window.get_ui_manager()
        manager.remove_ui(self._ui_id)
        manager.remove_action_group(self._action_group)
        manager.ensure_update()

    def do_update_state(self):
        view = self.get_view_activatable(self.window.get_active_view())
        self.get_action().set_active(view != None and view.enabled())

    def get_view_activatable(self, view):
        if not hasattr(view, "multiedit_view_activatable"):
            return None
        return view.multiedit_view_activatable

    def get_action(self):
        return self._action_group.get_action('MultiEditModeAction')

    def on_multi_edit_toggled(self, viewactivatable):
        if viewactivatable.view == self.window.get_active_view():
            self.get_action().set_active(viewactivatable.enabled())

    def on_multi_edit_mode(self, action):
        view = self.window.get_active_view()
        helper = self.get_view_activatable(view)

        if helper != None:
            helper.toggle_multi_edit(self.get_action().get_active())

