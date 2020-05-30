import configparser
import pathlib


def make_importable(import_name, theme_name):

	theme_index_path = pathlib.Path(__file__).parent.absolute() / import_name / theme_name / "index.theme"
	print(theme_index_path)
	theme_content_root = theme_index_path.parent.absolute()

	parser = configparser.ConfigParser()
	parser.read(theme_index_path)

	directories = parser.get("Icon Theme", "Directories").split(",")

	for directory in directories:
		if directory:
			base_path = theme_content_root
			for element in directory.split("/"):
				if not (base_path / element).is_dir():
					(base_path / element).mkdir()

				open(base_path / element / "__init__.py", "w").close()
				base_path = base_path / element
