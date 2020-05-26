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
#  Copyright 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
import pathlib
import subprocess
import sys
import tempfile
import xml.sax

# 3rd party
from lxml import etree
from scour import scour

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
	elif output == b"Emergency save activated!":
		raise IOError("Something went wrong")
	
	output += process.stdout.read(1)
	while output != b'\n>':
		output += process.stdout.read(1)
		output = output[1:]
		if output == b"Emergency save activated!":
			raise IOError("Something went wrong")


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
	print(rect, icon_file)
	
	cmd = [
			str(icon_file),
			# '--export-dpi', str(dpi),
			'-i', rect,
			'-l', str(output_file),
			]
	
	wait_for_prompt(inkscape_process, ' '.join(cmd))


class ScourOptions:
	strip_xml_prolog = False
	remove_titles = True
	remove_descriptions = True
	remove_metadata = True
	strip_comments = True
	embed_rasters = True
	enable_viewboxing = True
	indent_type = "none"
	indent_depth = 1
	newlines = False
	strip_ids = True
	shorten_ids = True
	

INKSCAPE = "http://www.inkscape.org/namespaces/inkscape"
SVG = "http://www.w3.org/2000/svg"


def get_layer_ids_by_name(input_file, layer_name):
	tree = etree.parse(str(input_file))
	
	# Find all layers
	all_layers = tree.findall(
			".//svg:g[@inkscape:groupmode=\"layer\"]",
			namespaces={"svg": SVG, "inkscape": INKSCAPE}
			)
	
	layer_ids = []
	
	for layer in all_layers:
		layer_label = layer.get(f"{{{INKSCAPE}}}label")
		if layer_label:
			if layer_label.startswith(layer_name):
				layer_id = layer.get("id")
				if layer_id:
					layer_ids.append(layer_id)
					
	return layer_ids


def check_id_in_svg(input_file, id):
	tree = etree.parse(str(input_file))
	results = tree.findall(f".//svg:g[@id=\"{id}\"]", namespaces={"svg": SVG})
	return bool(len(results))


def select_layer(input_file, tmp_file, icon_name):
	global inkscape_process
	if inkscape_process is None:
		inkscape_process = start_inkscape()
		
	# Read SVG file
	icon_layer_ids = get_layer_ids_by_name(input_file, icon_name)
	
	print(icon_layer_ids)
	
	# Double check that there isn't an exact match for the layer:
	tree = etree.parse(str(input_file))
	
	for layer_id in icon_layer_ids:
		layer = tree.findall(f".//svg:g[@id=\"{layer_id}\"]", namespaces={"svg": SVG})[0]
		if layer.get(f"{{{INKSCAPE}}}label") == icon_name:
			icon_layer_ids = [layer_id]
			break
	
	print(icon_layer_ids)
	print("\n")
	
	# Get layer ids for hires layers, as we'll need them later
	hires_layer_ids = get_layer_ids_by_name(input_file, "hires")
	
	if icon_layer_ids:
		if icon_layer_ids[0]:
			
			cmd = [
					str(input_file),
					# '--export-dpi', str(dpi), # TODO
					'--export-id', icon_layer_ids[0],
					'--export-plain-svg', str(tmp_file),
					"--export-id-only",
					]
			
			wait_for_prompt(inkscape_process, ' '.join(cmd))
	#
	# elif len(hires_layer_ids) == 1:
	#
	# 	cmd = [
	# 			str(input_file),
	# 			# '--export-dpi', str(dpi), # TODO
	# 			'--export-id', hires_layer_ids[0],
	# 			'--export-plain-svg', str(tmp_file),
	# 			"--export-id-only"
	# 			]
	#
	# 	wait_for_prompt(inkscape_process, ' '.join(cmd))
	
	return hires_layer_ids
	

def select_only_hires(input_file, tmp_file, hires_layer_ids):
	for layer_id in hires_layer_ids:
		if check_id_in_svg(input_file, layer_id):
	
			global inkscape_process
			if inkscape_process is None:
				inkscape_process = start_inkscape()
			
			cmd = [
					str(input_file),
					# '--export-dpi', str(dpi), # TODO
					'--export-id', layer_id,
					'--export-plain-svg', str(tmp_file),
					"--export-id-only",
					"--export-area-page",
					]
			
			wait_for_prompt(inkscape_process, ' '.join(cmd))
			
			return 1
	
	return 0


def minify_svg(input_file, output_file):
	# Read SVG file
	svg_string = pathlib.Path(input_file).read_text()

	# use scour to remove redundant stuff and then write to file
	svg_string = scour.scourString(svg_string, ScourOptions())
	
	with open(output_file, "w") as fp:
		fp.write(svg_string)
	

def make_svg_from_source(input_file, output_file, icon_name, dpi, id):
	with tempfile.TemporaryDirectory() as tmp_dir:
		tmp_dir = pathlib.Path(tmp_dir)
		
		tmp_svg = tmp_dir / f"{icon_name}.svg"
	
		hires_layer_ids = select_layer(input_file, tmp_svg, icon_name)
		if not tmp_svg.exists():
			# Wasn't a multi-image svg
			inkscape_export_svg(input_file, id, dpi, tmp_svg)
		else:
			inkscape_export_svg(tmp_svg, id, dpi, tmp_svg)
		print(253, tmp_svg)
		select_only_hires(tmp_svg, tmp_svg, hires_layer_ids)
		print(255, tmp_svg)
		minify_svg(tmp_svg, output_file)
	

def render_icon(infile, outfile, icon_name, dpi, id, scalable):
	if scalable:
		make_svg_from_source(infile, outfile, icon_name, dpi, id)
	else:
		inkscape_render_rect(infile, id, dpi, outfile)
	sys.stdout.write('.')


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
						
						directory = os.path.join(output_dir, size_str, self.context)
						
						scalable = bool(f"{size_str}/{self.context}" in scalable_directories)
						
						svg_file = os.path.join(directory, self.icon_name + '.svg')
						png_file = os.path.join(directory, self.icon_name + '.png')
						
						if not os.path.exists(directory):
							os.makedirs(directory)
						
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
						
							try:
								render_icon(self.path, outfile, self.icon_name, dpi, id, scalable)
							except IOError:
								print(f"Unable to process {self.path}.")
								continue
						else:
							stat_in = os.stat(self.path)
							stat_out = os.stat(outfile)
							if stat_in.st_mtime > stat_out.st_mtime:
								render_icon(self.path, outfile, self.icon_name, dpi, id, scalable)
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
