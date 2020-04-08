#!/usr/bin/python3
#
"""
Shared tools for building packages
"""
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
import os
import pathlib


author = "Dominic Davis-Foster"
author_email = "dominic@davis-foster.co.uk"
github_username = "domdfcoding"
web = github_url = f"https://github.com/{github_username}/custom_wx_icons"
copyright = """
2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
"""

general_trove_classifiers = [
		# "Environment :: MacOS X",
		# "Operating System :: MacOS :: MacOS X",
		
		# "Environment :: Win32 (MS Windows)",
		# "Operating System :: Microsoft :: Windows",
		# "Operating System :: Microsoft :: Windows :: Windows 10",
		# "Operating System :: Microsoft :: Windows :: Windows 7",
		# "Operating System :: Microsoft :: Windows :: Windows 8.1",
		
		"Operating System :: POSIX :: Linux",
		"Topic :: Desktop Environment :: Gnome",
		"Environment :: X11 Applications :: GTK",
		
		# "Operating System :: OS Independent",
		
		"Intended Audience :: Developers",
		
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3 :: Only",
		"Programming Language :: Python :: Implementation :: CPython",
		
		"Topic :: Software Development :: Libraries :: Python Modules",
		"Topic :: Software Development :: User Interfaces",
		]


def prepare_data_files(modname, theme_name):
	data_files = []
	
	theme_index_path = pathlib.Path(f"{modname}/{theme_name}/index.theme").absolute()
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
			
			abs_dir_path = (theme_content_root / directory)
			rel_dir_path = abs_dir_path.relative_to(pathlib.Path.cwd() / modname)
			
			data_files += [str(rel_dir_path / x) for x in os.listdir(abs_dir_path)]
	
	data_files.append(str(theme_index_path.relative_to(pathlib.Path.cwd() / modname)))
	
	return data_files


def get_requirements_and_readme(cwd):
	# Get info from files; set: long_description
	if cwd.name == "doc-source":
		install_requires = (cwd.parent / "requirements.txt").read_text().split("\n")
		long_description = (cwd.parent / "README.rst").read_text() + '\n'
	else:
		install_requires = pathlib.Path("requirements.txt").read_text().split("\n")
		long_description = pathlib.Path("README.rst").read_text() + '\n'
	
	return install_requires, long_description