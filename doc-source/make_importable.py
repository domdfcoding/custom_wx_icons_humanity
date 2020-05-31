import configparser
import pathlib


def make_importable(import_name, theme_name):

	theme_index_path = pathlib.Path(import_name).absolute() / theme_name / "index.theme"
	assert theme_index_path.is_file()

	theme_content_root = theme_index_path.parent.absolute()

	parser = configparser.ConfigParser()
	parser.read(theme_index_path)

	directories = parser.get("Icon Theme", "Directories").split(",")

	for directory in directories:
		if directory:
			base_path = theme_content_root
			for element in directory.split("/"):
				subdir = base_path / element
				if not subdir.is_dir():
					subdir.mkdir()

				init = subdir / '__init__.py'
				print(f"Creating {init}")
				init.open("w").close()
				base_path = subdir

	print(f"Creating {theme_content_root / '__init__.py'}")
	open(theme_content_root / "__init__.py", "w").close()


if __name__ == '__main__':
	make_importable("wx_icons_humanity", "Humanity")
	make_importable("wx_icons_humanity", "Humanity_Dark")
