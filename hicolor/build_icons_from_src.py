#!/usr/bin/python3
#
"""
Script to chop up SVGs into individual sizes

This takes around 15 minutes to run so be patient.
"""
#  
#  Based on `render-icon-theme.py` from the GNOME Project's adwaita-icon-theme
#  https://github.com/GNOME/adwaita-icon-theme
#  http://www.gnome.org
#
#  Also based on `render-bitmaps.py` from Ubuntu's Suru Icon Theme
#  https://github.com/ubuntu/yaru/blob/master/icons
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
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

# this package
from gnome_icon_builder import get_scalable_directories, main
from wx_icons_hicolor import theme_index_path

scalable_directories = get_scalable_directories(theme_index_path)


output_dir = "./wx_icons_hicolor/Hicolor"

# DPI multipliers to render at
dpis = [1]


main(os.path.join('.', 'svg_src'), dpis, output_dir, scalable_directories)
