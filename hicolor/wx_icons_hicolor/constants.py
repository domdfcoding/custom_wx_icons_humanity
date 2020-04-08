# stdlib
import pathlib

# 3rd party
import importlib_resources
import magic

# this package
from wx_icons_hicolor import Hicolor

mime = magic.Magic(mime=True)

with importlib_resources.path(Hicolor, "index.theme") as theme_index_path:
	theme_index_path = str(theme_index_path)
