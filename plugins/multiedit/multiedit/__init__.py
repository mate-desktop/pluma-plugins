# -*- coding: utf-8 -*-
#
# multiedit.py - Multi Edit
#
# Copyright (C) 2009 - Jesse van den Kieboom
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

import gi
gi.require_version('Pluma', '1.0')
gi.require_version('Gtk', '3.0')
gi.require_version('PangoCairo', '1.0')

from .viewactivatable import MultiEditViewActivatable
from .windowactivatable import MultiEditWindowActivatable

