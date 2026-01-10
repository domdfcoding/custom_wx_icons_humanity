#!/usr/bin/python3
#
#  __init__.py
"""
Humanity icon theme for wxPython.
"""
#
#  Copyright (C) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Includes icons from the Humanity and Humanity_Dark Icon Themes
#  https://launchpad.net/ubuntu/+archive/primary/+sourcefiles/humanity-icon-theme/0.6.15/humanity-icon-theme_0.6.15.tar.xz
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License version 2 as
#  published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# Humanity Colours
# https://drive.google.com/u/0/uc?id=0B7iDWdwgu9QAcDhUVXVvMVlLbEE&export=download

# stdlib
from typing import Any, Optional, Tuple, Union

# 3rd party
import importlib_resources
import wx  # type: ignore[import-not-found]
from wx_icons_adwaita import AdwaitaIconTheme, wxAdwaitaIconTheme
from wx_icons_hicolor import Icon

# this package
from wx_icons_humanity import Humanity, Humanity_Dark

__all__ = [
		"HumanityDarkIconTheme",
		"HumanityIconTheme",
		"version",
		"wxHumanityDarkIconTheme",
		"wxHumanityIconTheme",
		]

with importlib_resources.path(Humanity, "index.theme") as theme_index_path_:
	theme_index_path = str(theme_index_path_)

with importlib_resources.path(Humanity_Dark, "index.theme") as dark_theme_index_path_:
	dark_theme_index_path = str(dark_theme_index_path_)

__version__ = "0.1.3"


def version() -> str:
	"""
	Returns the version of this package and the icon theme, formatted for printing.
	"""

	return f"""wx_icons_humanity
Version {__version__}
Humanity Icon Theme Version 0.6.15
"""


class HumanityIconTheme(AdwaitaIconTheme):  # noqa: D101
	_adwaita_theme = AdwaitaIconTheme.create()

	@classmethod
	def create(cls) -> "HumanityIconTheme":
		"""
		Create an instance of the Humanity Icon Theme.
		"""

		with importlib_resources.path(Humanity, "index.theme") as theme_index_path_:
			theme_index_path = str(theme_index_path_)

		return cls.from_configparser(theme_index_path)

	def find_icon(  # noqa: D102
			self,
			icon_name: str,
			size: int,
			scale: Any,
			prefer_this_theme: bool = True,
			) -> Optional[Icon]:

		icon = self._do_find_icon(icon_name, size, scale, prefer_this_theme)
		if icon:
			return icon
		else:
			# If we get here we didn't find the icon.
			return self._adwaita_theme.find_icon(icon_name, size, scale)


class HumanityDarkIconTheme(HumanityIconTheme):  # noqa: D101
	_humanity_theme = HumanityIconTheme.create()

	@classmethod
	def create(cls) -> "HumanityDarkIconTheme":
		"""
		Create an instance of the Humanity Dark Icon Theme.
		"""

		with importlib_resources.path(Humanity_Dark, "index.theme") as theme_index_path_:
			theme_index_path = str(theme_index_path_)

		return cls.from_configparser(theme_index_path)

	def find_icon(  # noqa: D102
			self,
			icon_name: str,
			size: int,
			scale: Any,
			prefer_this_theme: bool = True,
			) -> Optional[Icon]:

		icon = self._do_find_icon(icon_name, size, scale, prefer_this_theme)
		if icon:
			return icon
		else:
			# If we get here we didn't find the icon.
			return self._humanity_theme.find_icon(icon_name, size, scale)


class wxHumanityIconTheme(wxAdwaitaIconTheme):  # noqa: D101
	_humanity_theme = HumanityIconTheme.create()

	def CreateBitmap(self, id: Any, client: Any, size: Union[Tuple[int], wx.Size]) -> wx.Bitmap:  # noqa: D102,A002  # pylint: disable=redefined-builtin
		icon = self._humanity_theme.find_icon(id, size[0], None)
		if icon:
			print(icon, icon.path)
			return self.icon2bitmap(icon, size[0])
		else:
			# return self._humanity_theme.find_icon("image-missing", size.x, None).as_bitmap()
			print("Icon not found in Humanity theme")
			print(id)
			return super().CreateBitmap(id, client, size)


class wxHumanityDarkIconTheme(wxHumanityIconTheme):  # noqa: D101
	_humanity_dark_theme = HumanityDarkIconTheme.create()

	def CreateBitmap(self, id: Any, client: Any, size: Union[Tuple[int], wx.Size]) -> wx.Bitmap:  # noqa: A002,D102  # pylint: disable=redefined-builtin
		icon = self._humanity_dark_theme.find_icon(id, size[0], None)
		if icon:
			print(icon, icon.path)
			return self.icon2bitmap(icon, size[0])
		else:
			# return self._humanity_dark_theme.find_icon("image-missing", size.x, None).as_bitmap()
			print("Icon not found in Humanity Dark theme")
			print(id)
			return super().CreateBitmap(id, client, size)


if __name__ == "__main__":

	theme = HumanityIconTheme.create()

	# for directory in theme.directories:
	# 	print(directory.icons)

	# icon = theme.find_icon("appointment-new", 48, None)
	# print(icon, icon.path)
	# 3rd party
	# from wx_icons_hicolor import test, test_random_icons
	from wx_icons_hicolor import test

	# test_random_icons(theme)
	test.test_icon_theme(theme, show_success=False)
