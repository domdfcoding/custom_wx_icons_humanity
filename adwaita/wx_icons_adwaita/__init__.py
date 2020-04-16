#!/usr/bin/python3
#
#  __init__.py
#
#  Copyright (C) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Includes icons from the Adwaita Icon Theme
#  https://launchpad.net/ubuntu/+archive/primary/+sourcefiles/adwaita-icon-theme/3.28.0-1ubuntu1/adwaita-icon-theme_3.28.0.orig.tar.xz
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
from wx_icons_adwaita import Adwaita
from wx_icons_hicolor import HicolorIconTheme, wxHicolorIconTheme


__version__ = "0.1.1"


def version():
	return f"""wx_icons_adwaita
Version {__version__}
Adwaita Icon Theme Version 3.28.0
"""


with importlib_resources.path(Adwaita, "index.theme") as theme_index_path:
	theme_index_path = str(theme_index_path)


class AdwaitaIconTheme(HicolorIconTheme):
	_hicolor_theme = HicolorIconTheme.create()

	@classmethod
	def create(cls):
		"""
		Create an instance of the Adwaita Icon Theme
		"""
		
		with importlib_resources.path(Adwaita, "index.theme") as theme_index_path:
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


class wxAdwaitaIconTheme(wxHicolorIconTheme):
	_adwaita_theme = AdwaitaIconTheme.create()
	
	def CreateBitmap(self, id, client, size):
		icon = self._adwaita_theme.find_icon(id, size.x, None)
		if icon:
			print(icon, icon.path)
			return self.icon2bitmap(icon, size.x)
		else:
			# return self._humanity_theme.find_icon("image-missing", size.x, None).as_bitmap()
			print("Icon not found in Adwaita theme")
			print(id)
			return super().CreateBitmap(id, client, size)


if __name__ == '__main__':
	# theme = AdwaitaIconTheme.from_configparser(theme_index_path)
	theme = AdwaitaIconTheme.create()
	
	# for directory in theme.directories:
	# 	print(directory.icons)
	
	from wx_icons_hicolor import test_random_icons, test
	# test_random_icons(theme)
	test.test_icon_theme(theme, show_success=False)
