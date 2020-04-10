#!/usr/bin/python3
#
"""
Script to chop up SVGs into individual sizes
"""
#  
#  Copyright (C) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License version 3 as
#  published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#


# stdlib
import os
import sys

sys.path.append(".")
sys.path.append("..")
sys.path.append("../hicolor")
sys.path.append("../adwaita")
sys.path.append("../humanity")

# this package
from gnome_icon_builder import get_scalable_directories, main
from wx_icons_suru import theme_index_path


scalable_directories = get_scalable_directories(theme_index_path)

SOURCES = ('actions', 'apps', 'categories', 'devices', 'emblems', 'legacy', 'mimetypes', 'places', 'status', 'wip')
output_dir = "./wx_icons_suru/Suru"

# DPI multipliers to render at
dpis = [1, 2]


for source in SOURCES:
	main(os.path.join('.', 'svg_src', source), dpis, output_dir, scalable_directories)
