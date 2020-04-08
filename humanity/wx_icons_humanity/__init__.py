# Humanity
# https://launchpad.net/ubuntu/+archive/primary/+sourcefiles/humanity-icon-theme/0.6.15/humanity-icon-theme_0.6.15.tar.xz

# Humanity Colours
# https://drive.google.com/u/0/uc?id=0B7iDWdwgu9QAcDhUVXVvMVlLbEE&export=download


# 3rd party
import importlib_resources

# this package
from wx_icons_adwaita import AdwaitaIconTheme, wxAdwaitaIconTheme
from wx_icons_humanity import Humanity, Humanity_Dark


with importlib_resources.path(Humanity, "index.theme") as theme_index_path:
	theme_index_path = str(theme_index_path)
	
with importlib_resources.path(Humanity_Dark, "index.theme") as dark_theme_index_path:
	dark_theme_index_path = str(dark_theme_index_path)


class HumanityIconTheme(AdwaitaIconTheme):
	_adwaita_theme = AdwaitaIconTheme.create()
	
	@classmethod
	def create(cls):
		"""
		Create an instance of the Humanity Icon Theme
		"""
		
		with importlib_resources.path(Humanity, "index.theme") as theme_index_path:
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
			return self._adwaita_theme.find_icon(icon_name, size, scale)
	

class HumanityDarkIconTheme(HumanityIconTheme):
	_humanity_theme = HumanityIconTheme.create()
	
	@classmethod
	def create(cls):
		"""
		Create an instance of the Humanity Dark Icon Theme
		"""
		
		with importlib_resources.path(Humanity_Dark, "index.theme") as theme_index_path:
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
	

class wxHumanityIconTheme(wxAdwaitaIconTheme):
	_humanity_theme = HumanityIconTheme.create()
	
	def CreateBitmap(self, id, client, size):
		icon = self._humanity_theme.find_icon(id, size.x, None)
		if icon:
			print(icon, icon.path)
			return self.icon2bitmap(icon, size.x)
		else:
			#return self._humanity_theme.find_icon("image-missing", size.x, None).as_bitmap()
			print("Icon not found in Humanity theme")
			print(id)
			return super().CreateBitmap(id, client, size)


class wxHumanityDarkIconTheme(wxHumanityIconTheme):
	_humanity_dark_theme = HumanityDarkIconTheme.create()
	
	def CreateBitmap(self, id, client, size):
		icon = self._humanity_dark_theme.find_icon(id, size.x, None)
		if icon:
			print(icon, icon.path)
			return self.icon2bitmap(icon, size.x)
		else:
			#return self._humanity_dark_theme.find_icon("image-missing", size.x, None).as_bitmap()
			print("Icon not found in Humanity Dark theme")
			print(id)
			return super().CreateBitmap(id, client, size)


if __name__ == '__main__':
	theme = HumanityIconTheme.create()
	
	# for directory in theme.directories:
	# 	print(directory.icons)
	
	icon = theme.find_icon("appointment-new", 48, None)
	print(icon, icon.path)
