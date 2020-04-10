#!/usr/bin/python3
#
#  icon_theme.py
#
#  Copyright (C) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
import configparser
import copy
import pathlib

# 3rd party
import importlib_resources

# this package
from wx_icons_hicolor import Hicolor
from .directory import Directory


class IconTheme:
	def __init__(self, name, comment, directories, inherits=None, scaled_directories=None, hidden=False, example=''):
		"""

		:param name: short name of the icon theme, used in e.g. lists when selecting themes.
		:type name: str
		:param comment: longer string describing the theme
		:type comment: str
		:param inherits: The name of the theme that this theme inherits from. If an icon name is not found
			in the current theme, it is searched for in the inherited theme (and recursively in all the
			inherited themes).

			If no theme is specified implementations are required to add the "hicolor" theme to the
			inheritance tree. An implementation may optionally add other default themes in between the last
			specified theme and the hicolor theme.
		:type inherits: list of str, optional
		:param directories: list of subdirectories for this theme. For every subdirectory there
			must be a section in the index.theme file describing that directory.
		:type directories: list of Directory objects
		:param scaled_directories: Additional list of subdirectories for this theme, in addition to the ones
			in Directories. These directories should only be read by implementations supporting scaled
			directories and was added to keep compatibility with old implementations that don't support these.
		:type scaled_directories: list of Directory objects, optional
		:param hidden: Whether to hide the theme in a theme selection user interface. This is used for things
			such as fallback-themes that are not supposed to be visible to the user.
		:type hidden: bool, optional
		:param example: The name of an icon that should be used as an example of how this theme looks.
		:type example: str, optional
		"""
		
		self.name = name
		self.comment = comment
		
		if not isinstance(directories, list) or not isinstance(directories[0], Directory):
			print(type(directories, type(directories[0])))
			raise TypeError("'directories' must be a list of Directory objects")
		self.directories = copy.deepcopy(directories)
		self.directories.sort(key=lambda directory: directory.size, reverse=True)
		
		if inherits:
			if not isinstance(inherits, list) or not isinstance(inherits[0], str):
				raise TypeError("'inherits' must be a list of strings")
			self.inherits = inherits
		else:
			self.inherits = []
		
		if scaled_directories:
			if not isinstance(scaled_directories, list) or not isinstance(scaled_directories[0], Directory):
				raise TypeError("'scaled_directories' must be a list of Directory objects")
			self.scaled_directories = scaled_directories
		else:
			self.scaled_directories = []
		
		self.hidden = hidden
		self.example = example
	
	def __iter__(self):
		for key, value in self.__dict__().items():
			yield key, value
	
	def __getstate__(self):
		return self.__dict__()
	
	def __setstate__(self, state):
		self.__init__(**state)
	
	def __dict__(self):
		return dict(
				name=self.name,
				comment=self.comment,
				directories=self.directories,
				inherits=self.inherits,
				scaled_directories=self.scaled_directories,
				hidden=self.hidden,
				example=self.example,
				)
	
	def __copy__(self):
		return self.__class__(**self.__dict__())
	
	def __deepcopy__(self, memodict={}):
		class_dict = self.__dict__()
		
		class_dict["directories"] = [copy.copy(directory) for directory in class_dict["directories"]]
		class_dict["scaled_directories"] = [copy.copy(directory) for directory in class_dict["scaled_directories"]]
		
		return self.__class__(**self.__dict__())
	
	def __repr__(self):
		return f"{self.name} Icon Theme object at {id(self)})"
	
	def __str__(self):
		return f"{self.name} Icon Theme"
	
	@classmethod
	def from_configparser(cls, theme_index_path):
		parser = configparser.ConfigParser()
		parser.read(theme_index_path)
		
		theme_content_root = pathlib.Path(theme_index_path).parent
		
		name = parser.get("Icon Theme", "Name")
		comment = parser.get("Icon Theme", "Comment")
		inherits = parser.get("Icon Theme", "Inherits", fallback='').split(",")
		
		directories = parser.get("Icon Theme", "Directories").split(",")
		while "" in directories:
			directories.remove("")
		
		directories_new = []
		
		for directory in directories:
			icon_dir = Directory.from_configparser(parser[directory], theme_content_root)
			icon_dir.theme = name
			directories_new.append(icon_dir)
			
		scaled_directories = parser.get("Icon Theme", "ScaledDirectories", fallback='').split(",")
		while "" in scaled_directories:
			scaled_directories.remove("")
		
		scaled_directories_new = []
		
		for directory in scaled_directories:
			icon_dir = Directory.from_configparser(parser[directory], theme_content_root)
			icon_dir.theme = name
			scaled_directories_new.append(icon_dir)
		
		hidden = parser.getboolean("Icon Theme", "Hidden", fallback=False)
		example = parser.get("Icon Theme", "Example", fallback='')
		
		# print(name)
		# print(comment)
		# print(inherits)
		# print(directories)
		# print(scaled_directories)
		# print(hidden)
		# print(example)
		
		return cls(name, comment, directories_new, inherits, scaled_directories_new, hidden, example)
	
	def _do_find_icon(self, icon_name, size, scale, prefer_this_theme=True):
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
		# TODO: scale
		
		smallest_size_available = 0
		largest_size_available = 0
		
		# possible_icons = []
		
		for directory in self.directories:
			# print(directory)
			
			if icon_name in directory.icons:
				for icon in directory.icons:
					if icon.name == icon_name:
						
						if directory.type == "Scalable":
							if directory.min_size == directory.size or (size >= directory.min_size):
								if (directory.max_size == directory.size) or (size <= directory.max_size):
									return icon
						
						else:
							if directory.size == size:
								return icon
						
						if prefer_this_theme:
							if largest_size_available:
								if directory.max_size > largest_size_available:
									largest_size_available = directory.max_size
							else:
								largest_size_available = directory.max_size
							
							if smallest_size_available:
								if directory.min_size < smallest_size_available:
									smallest_size_available = directory.min_size
							else:
								smallest_size_available = directory.min_size
		
		# If we get here we didn't find the icon.
		if prefer_this_theme:
			if largest_size_available and size > largest_size_available:
				return self.find_icon(icon_name, largest_size_available, scale, False)
			elif smallest_size_available and size < smallest_size_available:
				return self.find_icon(icon_name, smallest_size_available, scale, False)
	
	def find_icon(self, icon_name, size, scale, prefer_this_theme=True):
		"""
		Searches for the icon with the given name and size.
		
		:param icon_name: The name of the icon to find.
			Any `FreeDesktop Icon Theme Specification <https://specifications.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html>`_
			name can be used.
		:type icon_name: str
		:param size: The desired size of the icon
		:type size: int
		:param scale: TODO: Currently does nothing
		:type scale: any
		:param prefer_this_theme: Return an icon from this theme even if it has to be resized,
			rather than a correctly sized icon from the parent theme.
		:type prefer_this_theme:
		
		:return: The icon if it was found, or None
		:rtype: Icon or None
		"""
		
		icon = self._do_find_icon(icon_name, size, scale, prefer_this_theme)
		if icon:
			return icon
		else:
			# If we get here we didn't find the icon.
			return None
		
		
class HicolorIconTheme(IconTheme):
	@classmethod
	def create(cls):
		"""
		Create an instance of the Hicolor Icon Theme
		"""
		
		with importlib_resources.path(Hicolor, "index.theme") as theme_index_path:
			theme_index_path = str(theme_index_path)
		
		return cls.from_configparser(theme_index_path)

