#!/usr/bin/python3
#
#  __init__.py
#
#  Copyright (C) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Includes Public Domain icons from the Tango Project
#  https://launchpad.net/ubuntu/+archive/primary/+sourcefiles/tango-icon-theme/0.8.90-5ubuntu1/tango-icon-theme_0.8.90.orig.tar.gz
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


# 3rd party
import importlib_resources

# this package
from wx_icons_hicolor import HicolorIconTheme, wxHicolorIconTheme
from wx_icons_tango import Tango


with importlib_resources.path(Tango, "index.theme") as theme_index_path:
	theme_index_path = str(theme_index_path)

__version__ = "0.1.1"


def version():
	return f"""wx_icons_tango
Version {__version__}
Tango Icon Theme Version 0.8.90
"""


class TangoIconTheme(HicolorIconTheme):
	_hicolor_theme = HicolorIconTheme.create()
	
	@classmethod
	def create(cls):
		"""
		Create an instance of the Tango Icon Theme
		"""
		
		with importlib_resources.path(Tango, "index.theme") as theme_index_path:
			theme_index_path = str(theme_index_path)
		
		return cls.from_configparser(theme_index_path)
	
	def find_icon(self, icon_name, size, scale, prefer_this_theme=True):
		"""

		:param icon_name:
		:type icon_name:
		:param size:
		:type size:
		:param scale:
		:type scale:
		:param prefer_this_theme: Return an icon from this theme even if it has to be resized,
			rather than a correctly sized icon from the parent theme.
		:type prefer_this_theme:
		:return:
		:rtype:
		"""
		
		icon = self._do_find_icon(icon_name, size, scale, prefer_this_theme)
		if icon:
			return icon
		else:
			# If we get here we didn't find the icon.
			return self._hicolor_theme.find_icon(icon_name, size, scale)


class wxTangoIconTheme(wxHicolorIconTheme):
	_tango_theme = TangoIconTheme.create()
	
	def CreateBitmap(self, id, client, size):
		icon = self._tango_theme.find_icon(id, size.x, None)
		if icon:
			print(icon, icon.path)
			return self.icon2bitmap(icon, size.x)
		else:
			# return self._tango_theme.find_icon("image-missing", size.x, None).as_bitmap()
			print("Icon not found in Tango theme")
			print(id)
			return super().CreateBitmap(id, client, size)


if __name__ == '__main__':
	# theme = TangoIconTheme.from_configparser(theme_index_path)
	theme = TangoIconTheme.create()
	
	# for directory in theme.directories:
	# 	print(directory.icons)
	
	from wx_icons_hicolor import test_random_icons, test
	# test_random_icons(theme)
	test.test_icon_theme(theme, show_success=False)
