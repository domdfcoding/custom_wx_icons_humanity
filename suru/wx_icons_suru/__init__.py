# Suru
# https://github.com/ubuntu/yaru/blob/master/icons


# 3rd party
import importlib_resources

# this package
from wx_icons_suru import Suru
from wx_icons_humanity import HumanityIconTheme, wxHumanityIconTheme
from wx_icons_hicolor import test_random_icons


with importlib_resources.path(Suru, "index.theme") as theme_index_path:
	theme_index_path = str(theme_index_path)


__version__ = "0.0.0"


def version():
	return f"""wx_icons_hicolor
Version {__version__}
Gnome Icon Theme Version 20.04.4
"""


class SuruIconTheme(HumanityIconTheme):
	_humanity_theme = HumanityIconTheme.create()

	@classmethod
	def create(cls):
		"""
		Create an instance of the Suru Icon Theme
		"""
		
		with importlib_resources.path(Suru, "index.theme") as theme_index_path:
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
			return self._humanity_theme.find_icon(icon_name, size, scale)


class wxSuruIconTheme(wxHumanityIconTheme):
	_suru_theme = SuruIconTheme.create()
	
	def CreateBitmap(self, id, client, size):
		icon = self._suru_theme.find_icon(id, size.x, None)
		if icon:
			print(icon, icon.path)
			return self.icon2bitmap(icon, size.x)
		else:
			# return self._humanity_theme.find_icon("image-missing", size.x, None).as_bitmap()
			print("Icon not found in Suru theme")
			print(id)
			return super().CreateBitmap(id, client, size)


if __name__ == '__main__':
	# theme = SuruIconTheme.from_configparser(theme_index_path)
	theme = SuruIconTheme.create()
	
	# for directory in theme.directories:
	# 	print(directory.icons)
	
	test_random_icons(theme)
