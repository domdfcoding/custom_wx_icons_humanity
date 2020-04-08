# stdlib
import configparser
import pathlib

# this package
from .directory import Directory
from wx_icons_hicolor.constants import mime, theme_index_path
# stdlib
import pathlib

# 3rd party
import importlib_resources
import magic
import magic

# this package
from wx_icons_hicolor import Hicolor


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
			raise TypeError("'directories' must be a list of Directory objects")
		self.directories = directories
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
		directories = [Directory.from_configparser(parser[directory], theme_content_root) for directory in directories]
		
		scaled_directories = parser.get("Icon Theme", "ScaledDirectories", fallback='').split(",")
		while "" in scaled_directories:
			scaled_directories.remove("")
		scaled_directories = [
				Directory.from_configparser(
						parser[directory], theme_content_root
						) for directory in scaled_directories]
		
		hidden = parser.getboolean("Icon Theme", "Hidden", fallback=False)
		example = parser.get("Icon Theme", "Example", fallback='')
		
		# print(name)
		# print(comment)
		# print(inherits)
		# print(directories)
		# print(scaled_directories)
		# print(hidden)
		# print(example)
		
		return cls(name, comment, directories, inherits, scaled_directories, hidden, example)
	
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

