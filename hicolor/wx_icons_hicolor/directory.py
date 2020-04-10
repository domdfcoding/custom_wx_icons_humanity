#!/usr/bin/python3
#
#  directory.py
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
import pathlib

from memoized_property import memoized_property

# this package
from .constants import mime
from .icon import Icon


class Directory:
	def __init__(
			self, path, size, scale=1, context='', type='Threshold',
			max_size=None, min_size=None, threshold=2, theme=''):
		"""

		:param path: The absolute path to the directory
		:type path: str
		:param size: Nominal (unscaled) size of the icons in this directory.
		:type size: int
		:param scale: Target scale of of the icons in this directory. Defaults to the value 1 if not present.
			Any directory with a scale other than 1 should be listed in the ScaledDirectories list rather
			than Directories for backwards compatibility.
		:type scale: int, optional
		:param context: The context the icon is normally used in. This is in detail discussed in the section called “Context”.
		:type context: str
		:param type: The type of icon sizes for the icons in this directory.
			Valid types are Fixed, Scalable and Threshold.
			The type decides what other keys in the section are used.
			If not specified, the default is Threshold.
		:type type: str
		:param max_size: Specifies the maximum (unscaled) size that the icons in this directory can be scaled to. Defaults to the value of Size if not present.
		:type max_size: int
		:param min_size: Specifies the minimum (unscaled) size that the icons in this directory can be scaled to. Defaults to the value of Size if not present.
		:type min_size: int
		:param threshold: The icons in this directory can be used if the size differ at most this much from the desired (unscaled) size. Defaults to 2 if not present.
		:type threshold: int
		:param theme: The name of the theme this directory is a part of
		:type theme: str
		"""
		
		self.scale = scale
		self.context = context
		self.threshold = threshold
		self.theme = theme
		
		if not isinstance(path, pathlib.Path):
			raise TypeError("'path' must be a pathlib.Path object.")
		self.path = path
		
		if not isinstance(size, int):
			raise TypeError("'size' must be a integer.")
		self.size = size
		
		if type not in {"Fixed", "Scalable", "Threshold"}:
			raise ValueError("'type' must be one of 'Fixed', 'Scalable' or 'Threshold'.")
		self.type = type
		
		if max_size:
			if not isinstance(max_size, int):
				raise TypeError("'max_size' must be a integer.")
			self.max_size = max_size
		else:
			self.max_size = size
		
		if min_size:
			if not isinstance(min_size, int):
				raise TypeError("'min_size' must be a integer.")
			self.min_size = min_size
		else:
			self.min_size = size
	
	def __iter__(self):
		for key, value in self.__dict__().items():
			yield key, value
	
	def __getstate__(self):
		return self.__dict__()
	
	def __setstate__(self, state):
		self.__init__(**state)
	
	def __dict__(self):
		return dict(
				path=self.path,
				size=self.size,
				scale=self.scale,
				context=self.context,
				type=self.type,
				max_size=self.max_size,
				min_size=self.min_size,
				threshold=self.threshold,
				theme=self.theme,
				)
	
	def __copy__(self):
		return self.__class__(**self.__dict__())
	
	def __deepcopy__(self, memodict={}):
		return self.__copy__()
	
	@classmethod
	def from_configparser(cls, config_section, theme_content_root):
		if not isinstance(config_section, configparser.SectionProxy):
			raise TypeError("'config_section' must be a 'configparser.SectionProxy' object")
		
		path = theme_content_root / pathlib.Path(config_section.name)
		size = int(config_section.get("Size"))
		scale = int(config_section.get("Scale", fallback=1))
		context = config_section.get("Context", fallback='')
		type = config_section.get("Type", fallback='Threshold')
		max_size = config_section.get("MaxSize", fallback=None)
		if max_size:
			max_size = int(max_size)
		min_size = config_section.get("MinSize", fallback=None)
		if min_size:
			min_size = int(min_size)
		threshold = int(config_section.get("Threshold", fallback=2))
		
		return cls(path, size, scale, context, type, max_size, min_size, threshold)
	
	@memoized_property
	def icons(self):
		absolute_dir_path = self.path.resolve()
		# print(absolute_dir_path)
		
		icons = []
		
		for item in absolute_dir_path.iterdir():
			if item.is_file():
				if mime.from_file(str(item.resolve())) in {"image/svg+xml", "image/png"}:
					icon = Icon(item.stem, item, self.size, self.type, self.max_size, self.min_size, self.theme)
					icons.append(icon)
		
		return icons
	
	def __repr__(self):
		return f"Directory({self.path})"
	
	def __str__(self):
		return self.__repr__()
