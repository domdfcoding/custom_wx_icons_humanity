#!/usr/bin/python3
#
"""
Function to chop up SVGs into individual sizes

Don't call this directly. Instead, use it in your build script.

e.g.
>>> import os
>>> from gnome_icon_builder import main, get_scalable_directories
>>> from wx_icons_suru import theme_index_path
>>>
>>> SOURCES = ('actions', 'apps', 'categories')
>>> output_dir = "./Suru"
>>>
>>> # DPI multipliers to render at
>>> dpis = [1, 2]
>>>
>>> scalable_directories = get_scalable_directories(theme_index_path)
>>>
>>> for source in SOURCES:
... 	main(os.path.join('.', 'svg_src', source), dpis, output_dir, scalable_directories)
>>>
"""
#
#  Based on `render-icon-theme.py` from the GNOME Project's adwaita-icon-theme
#  https://github.com/GNOME/adwaita-icon-theme
#  http://www.gnome.org
#
#  Also based on `render-bitmaps.py` from Ubuntu's Suru Icon Theme
#  https://github.com/ubuntu/yaru/blob/master/icons
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
import subprocess
import sys
import xml.sax


OPTIPNG = '/usr/bin/optipng'
inkscape_process = None


def get_scalable_directories(theme_index_path):
	parser = configparser.ConfigParser()
	parser.read(theme_index_path)
	
	directories = parser.get("Icon Theme", "Directories").split(",")
	
	scalable_directories = []
	
	for directory in directories:
		if directory:
			if parser.get(directory, "Type") == "Scalable":
				scalable_directories.append(directory)
	
	return scalable_directories


def optimize_png(png_file):
	if os.path.exists(OPTIPNG):
		process = subprocess.Popen([OPTIPNG, '-quiet', '-o7', png_file])
		process.wait()
	
	
def wait_for_prompt(process, command=None):
	if command is not None:
		process.stdin.write((command + '\n').encode('utf-8'))
	
	# This is kinda ugly ...
	# Wait for just a '>', or '\n>' if some other char appearead first
	output = process.stdout.read(1)
	if output == b'>':
		return
	
	output += process.stdout.read(1)
	while output != b'\n>':
		output += process.stdout.read(1)
		output = output[1:]


def start_inkscape():
	process = subprocess.Popen(['inkscape', '--shell'], bufsize=0, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	wait_for_prompt(process)
	return process
	
	
def inkscape_render_rect(icon_file, rect, dpi, output_file):
	global inkscape_process
	if inkscape_process is None:
		inkscape_process = start_inkscape()
	
	cmd = [
			icon_file,
			'--export-dpi', str(dpi),
			'-i', rect,
			'-e', output_file,
			]
	
	wait_for_prompt(inkscape_process, ' '.join(cmd))
	optimize_png(output_file)


def inkscape_export_svg(icon_file, rect, dpi, output_file):
	global inkscape_process
	if inkscape_process is None:
		inkscape_process = start_inkscape()
	
	cmd = [
			icon_file,
			'--export-dpi', str(dpi),
			'-i', rect,
			'-l', output_file,
			]
	
	wait_for_prompt(inkscape_process, ' '.join(cmd))


def main(source_dir, dpis, output_dir, scalable_directories):
	
	class ContentHandler(xml.sax.ContentHandler):
		ROOT = 0
		SVG = 1
		LAYER = 2
		OTHER = 3
		TEXT = 4
		
		def __init__(self, path, force=False, filter=None):
			self.stack = [self.ROOT]
			self.inside = [self.ROOT]
			self.path = path
			self.rects = []
			self.state = self.ROOT
			self.chars = ""
			self.force = force
			self.filter = filter
		
		def endDocument(self):
			pass
		
		def startElement(self, name, attrs):
			if self.inside[-1] == self.ROOT:
				if name == "svg":
					self.stack.append(self.SVG)
					self.inside.append(self.SVG)
					return
			elif self.inside[-1] == self.SVG:
				if (name == "g" and ('inkscape:groupmode' in attrs) and ('inkscape:label' in attrs)
						and attrs['inkscape:groupmode'] == 'layer' and attrs['inkscape:label'].lower().startswith(
								'baseplate')):
					self.stack.append(self.LAYER)
					self.inside.append(self.LAYER)
					self.context = None
					self.icon_name = None
					self.rects = []
					return
			elif self.inside[-1] == self.LAYER:
				if name == "text" and ('inkscape:label' in attrs) and attrs['inkscape:label'] == 'context':
					self.stack.append(self.TEXT)
					self.inside.append(self.TEXT)
					self.text = 'context'
					self.chars = ""
					return
				elif name == "text" and ('inkscape:label' in attrs) and attrs['inkscape:label'] == 'icon-name':
					self.stack.append(self.TEXT)
					self.inside.append(self.TEXT)
					self.text = 'icon-name'
					self.chars = ""
					return
				elif name == "rect":
					self.rects.append(attrs)
			
			self.stack.append(self.OTHER)
		
		def endElement(self, name):
			stacked = self.stack.pop()
			
			if self.inside[-1] == stacked:
				self.inside.pop()
			
			if stacked == self.TEXT and self.text is not None:
				assert self.text in ['context', 'icon-name']
				if self.text == 'context':
					self.context = self.chars
				elif self.text == 'icon-name':
					self.icon_name = self.chars
				self.text = None
			elif stacked == self.LAYER:
				assert self.icon_name
				assert self.context
				
				if self.filter is not None and self.icon_name not in self.filter:
					return
				
				print(self.context, self.icon_name)
				
				# TODO: Check that all sizes are available, and if not use the largest size available for the missing sizes
				
				for rect in self.rects:
					for dpi_factor in dpis:
						width = int(float(rect['width']))
						height = int(float(rect['height']))
						id = rect['id']
						dpi = 96 * dpi_factor
						
						size_str = "%sx%s" % (width, height)
						if dpi_factor != 1:
							size_str += "@%sx" % dpi_factor
						
						dir = os.path.join(output_dir, size_str, self.context)
						
						if f"{size_str}/{self.context}" in scalable_directories:
							scalable = True
						else:
							scalable = False
							
						svg_file = os.path.join(dir, self.icon_name + '.svg')
						png_file = os.path.join(dir, self.icon_name + '.png')
						
						if not os.path.exists(dir):
							os.makedirs(dir)
						
						if scalable:
							if os.path.isfile(png_file):
								os.unlink(png_file)
							outfile = svg_file
						else:
							if os.path.isfile(svg_file):
								os.unlink(svg_file)
							outfile = png_file
							
						# Do a time based check!
						if self.force or not os.path.exists(outfile):
							if scalable:
								inkscape_export_svg(self.path, id, dpi, outfile)
							else:
								inkscape_render_rect(self.path, id, dpi, outfile)
							sys.stdout.write('.')
						else:
							stat_in = os.stat(self.path)
							stat_out = os.stat(outfile)
							if stat_in.st_mtime > stat_out.st_mtime:
								if scalable:
									inkscape_export_svg(self.path, id, dpi, outfile)
								else:
									inkscape_render_rect(self.path, id, dpi, outfile)
								sys.stdout.write('.')
							else:
								sys.stdout.write('-')
						sys.stdout.flush()
				sys.stdout.write('\n')
				sys.stdout.flush()
		
		def characters(self, chars):
			self.chars += chars.strip()
	
	if len(sys.argv) == 1:
		if not os.path.exists(output_dir):
			os.mkdir(output_dir)
		open(os.path.join(output_dir, "__init__.py"), "w").close()
		print('Rendering from SVGs in', source_dir)
		for file in os.listdir(source_dir):
			if file[-4:] == '.svg':
				file = os.path.join(source_dir, file)
				handler = ContentHandler(file)
				xml.sax.parse(open(file), handler)
	else:
		file = os.path.join(source_dir, sys.argv[1] + '.svg')
		if len(sys.argv) > 2:
			icons = sys.argv[2:]
		else:
			icons = None
		if os.path.exists(os.path.join(file)):
			handler = ContentHandler(file, True, filter=icons)
			xml.sax.parse(open(file), handler)
		else:
			print("Error: No such file", file)
			sys.exit(1)
