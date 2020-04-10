#!/usr/bin/python3
#
#  icon.py
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
import pathlib
from io import BytesIO
import warnings
import base64

# 3rd party
import cairosvg
import wx

# this package
from .constants import mime


class Icon:
	def __init__(self, name, path, size, type='Threshold', max_size=None, min_size=None, theme=''):
		"""

		:param name: The name of the icon
		:type name: str
		:param path: The path to the icon
		:type path: pathlib.Path
		:param size: Nominal (unscaled) size of the icon.
		:type size: int
		:param type: The type of icon sizes for the icon.
			Valid types are Fixed, Scalable and Threshold.
			The type decides what other keys in the section are used.
			If not specified, the default is Threshold.
		:type type: str
		:param max_size: Specifies the maximum (unscaled) size that the icon can be scaled to. Defaults to the value of Size if not present.
		:type max_size: int
		:param min_size: Specifies the minimum (unscaled) size that the icon can be scaled to. Defaults to the value of Size if not present.
		:type min_size: int
		:param theme: The name of the theme this icon came from
		:type theme: str
		"""
		
		if not isinstance(path, pathlib.Path):
			raise TypeError("'path' must be a pathlib.Path object.")
		self.path = path.resolve()
		
		if self.mime_type not in {"image/svg+xml", "image/png"}:
			raise TypeError("The specified file is not a valid icon")
		
		self.name = name
		self.theme = theme
		
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
				name=self.name,
				path=self.path,
				size=self.size,
				type=self.type,
				max_size=self.max_size,
				min_size=self.min_size,
				theme=self.theme,
				)
	
	def __copy__(self):
		return self.__class__(**self.__dict__())
	
	def __deepcopy__(self, memodict={}):
		return self.__copy__()
	
	@property
	def mime_type(self):
		return mime.from_file(str(self.path))
	
	@property
	def scalable(self):
		if self.type == "Fixed" and self.mime_type == "image/png":
			return False
		return True
	
	def as_png(self, size=None):
		"""
		Returns the icon as a BytesIO object containing PNG image data
		
		:return:
		:rtype:
		"""
		
		if not size:
			size = self.size
			
		if self.mime_type == "image/png":
			with open(self.path, "rb") as fin:
				data = BytesIO(fin.read())
			return data
		
		elif self.mime_type == "image/svg+xml":
			svg_img = cairosvg.svg2png(url=str(self.path), output_width=size, output_height=size)
			return BytesIO(svg_img)
	
	def as_base64_png(self, size):
		"""
		Returns the icon as a base64-encoded BytesIO object containing PNG image data

		:return:
		:rtype:
		"""
		
		base64.b64encode(self.as_png(size).getvalue()).decode("utf-8")
	
	def as_bitmap(self, size=None):
		"""
		Returns the icon as a wxPython bitmap
		
		:rtype: wx.Bitmap
		"""
		
		if not size:
			size = self.size
		
		if not self.scalable:
			if size != self.size:
				raise ValueError("This icon cannot be scaled")

		if size > self.max_size:
			print(size, self.size, self.max_size)
			warnings.warn(f"This icon should not be scaled larger than {self.max_size} px")
		elif size < self.min_size:
			warnings.warn(f"This icon should not be scaled smaller than {self.min_size} px")
			
		if self.mime_type == "image/png":
			# TODO Scaling
			return wx.Bitmap(wx.Image(str(self.path), wx.BITMAP_TYPE_PNG))
		elif self.mime_type == "image/svg+xml":
			svg_img = cairosvg.svg2png(url=str(self.path), output_width=size, output_height=size)
			return wx.Bitmap(wx.Image(BytesIO(svg_img), wx.BITMAP_TYPE_PNG))
	
	def __repr__(self):
		return f"Icon({self.name})"
	
	def __str__(self):
		return self.__repr__()
	
	def __eq__(self, other):
		if isinstance(other, str):
			return self.name == other
		
		return NotImplemented
