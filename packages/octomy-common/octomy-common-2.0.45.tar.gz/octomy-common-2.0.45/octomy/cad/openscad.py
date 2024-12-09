from enum import Enum
import asyncio
import datetime
import octomy.utils
import logging
import os
import pprint
import re
import subprocess
import sys
import shlex

#1Br_h9krCj2cKFQ8GIo-xBU4ljUvhD7a_
logger = logging.getLogger(__name__)

####################################################### COMMON

# -12345.67890
decimal_number_inc = r'-?\d*\.?\d+'

# "some string"
quoted_string_inc = r'(["\'])(?P<value>(?:(?!\1).)*)\1'

# (mm)
unit_inc = r'(?:\s*\(\s*(?P<unit>[^\s]+)\s*\)\s*)'

####################################################### META

# /* [Section name] */
#h1_re = re.compile(r"^\/\*\s*\[\s*(?P<section>[^\[]+)\s*\]\s*\*\/", flags=re.MULTILINE)
h1_re = re.compile(r"^\/\*\s*\[\s*(?P<section>[^\]\s]+(?:[^\]]*[^\]\s])?)\s*\]\s*\*\/", flags=re.MULTILINE)

# // Variable description
#h2_re = re.compile(r'^\/\/\s*(?P<description>.*)\s*$', flags=re.MULTILINE)
h2_re = re.compile(r'^\s*\/\/\s*(?P<description>[^\s].*?)\s*' + unit_inc + r'?$')

# Variable = definition; // comment
#var_re = re.compile(r'^\s*(?P<variable>\w+)\s*=\s*(?P<value>[^;]+);(?:\s*\/\/\s*(?P<schema>[^\n]*))?\s*$', flags=re.MULTILINE)
var_re = re.compile(r'^\s*(?P<variable>.*?)\s*=\s*(?P<value>.*?)\s*;\s*(?:\s*\/\/\s*(?P<comment>.*?)\s*)?$', flags=re.MULTILINE)


####################################################### VALUES

# true
bool_val_re = re.compile(r'\s*(?P<value>true|false)\s*')

# "mystring"
string_val_re = re.compile(r'\s*' + quoted_string_inc + r'\s*')

# -1234.56789
number_val_re = re.compile(r'\s*(?P<value>' + decimal_number_inc + r')\s*')

# [ 1,2,3,4,5 ]
#vector_val_re = re.compile(r'\s*\[\s*(?P<value>(?:' + decimal_number_inc + r'\s*,?\s*)+)\]\s*')
vector_val_re = re.compile(r'\s*\[\s*(?P<value>' + decimal_number_inc + r'(?:\s*,\s*' + decimal_number_inc + r')*)\]\s*')


####################################################### BOOL SCHEMA


# [ true:label1, false:label2]
#labeled_bool_schema_re = re.compile(r'\s*\[\s*(?P<values>(?:\s*(true|false)\:[\w\s]*)(?:\s*,\s*(true|false):[\w\s]*)*)\s*\]\s*')
labeled_bool_schema_re = re.compile(r'\s*\[\s*(?P<values>(?:\s*(true|false)\s*:\s*\w.*?)(?:\s*,\s*(true|false)\s*:\s*\w.*?)*)\s*\]\s*')


####################################################### STRINGS SCHEMA

# [ value1, value2, value3 ]
values_string_schema_re = re.compile(r'\s*\[\s*(?P<values>(?:[a-zA-Z]\w*)(?:\s*,\s*[a-zA-Z]\w*)*)\s*\]\s*')

# [ value1:label1, value3:label2, value3:label3 ]
#labeled_string_schema_re = re.compile(r'\s*\[\s*(?P<values>(?:[a-zA-Z]\w*\:[\w\s]*)(?:\s*,\s*[a-zA-Z]\w*:[\w\s]*)*)\s*\]\s*')
labeled_string_schema_re = re.compile(r'\s*\[\s*(?P<values>[a-zA-Z]\w*\s*:[^,\s].*?(?:\s*,\s*[a-zA-Z]\w*\s*:[^,\s].*?)*)\s*\]\s*')


####################################################### NUMBERS SCHEMA


# [ max ]
#range1_schema_re = re.compile(r'\s*(?P<max>' + decimal_number_inc + r')\s*\]\s*' + unit_inc + r'?')
range1_schema_re = re.compile(r'\s*\[\s*(?P<max>' + decimal_number_inc + r')\s*\]\s*' + unit_inc + r'?')

# [ min : max ]
range2_schema_re = re.compile(r'\s*\[\s*(?P<min>' + decimal_number_inc + r')\s*:\s*(?P<max>' + decimal_number_inc + r')\s*\]\s*' + unit_inc + r'?')

# [ min : step : max ]
range3_schema_re = re.compile(r'\s*\[\s*(?P<min>' + decimal_number_inc + r')\s*:\s*(?P<step>' + decimal_number_inc + r')\s*:\s*(?P<max>' + decimal_number_inc + r')\s*\]\s*' + unit_inc + r'?')

# [ 123:label1, 456:label2, 789:label3 ]
#labeled_number_schema_re = re.compile(r'\s*\[\s*(?P<values>(?:' + decimal_number_inc + r'\:[\w\s]*)(?:\s*,\s*' + decimal_number_inc + r':[\w\s]*)*)\s*\]\s*' + unit_inc + r'?')
labeled_number_schema_re = re.compile(r'\s*\[\s*(?P<values>(?:' + decimal_number_inc + r'\s*:\s*[^,\s].*?(?:\s*,\s*' + decimal_number_inc + r'\s*:\s*[^,\s].*?)*))\s*\]\s*' + unit_inc + r'?')

# [ 123, 456, 789 ]
values_number_schema_re = re.compile(r'\s*\[\s*(?P<values>' + decimal_number_inc + r'(?:\s*,\s*' + decimal_number_inc + r')*)\s*\]\s*' + unit_inc + r'?')


#######################################################

version_re = re.compile(r'OpenSCAD version\s*(?P<version>.*)\s*')

def parse_version(text):
	m = version_re.match(text)
	if m:
		g = m.groupdict()
		return g.get("version")
	return None


#######################################################



def now():
	return datetime.datetime.now(datetime.timezone.utc)

def millinow():
	tz = datetime.timezone.utc
	now = datetime.datetime.now(tz)
	epoch = datetime.datetime(1970, 1, 1, tzinfo = tz) # use POSIX epoch
	posix_timestamp_millis = (now - epoch) // datetime.timedelta(milliseconds=1) 
	return posix_timestamp_millis

def shex(raw):
	neat = shlex.quote(raw)
	if raw != neat:
		logger.info(f"SHEX {raw} -> {neat}")
	return neat

def parse_number(num_str):
	if not num_str:
		 # logger.warning(f"No string '{num_str}' to convert to number, returning 0");
		return 0
	num_str = num_str.strip().lower()
	try:
		num_int = int(num_str)
		#if str(num_int) == num_str:
		return num_int
	except:
		pass
	try:
		num_float = float(num_str)
		#if str(num_float) == num_str:
		return num_float
	except:
		pass
	logger.warning(f"Could not convert string '{num_str}' to number, returning 0");
	return 0

def parse_vector(raw):
	# logger.info(" parse_vector()")
	out = list()
	if raw:
		# logger.info(f"VECTOR RAW: {pprint.pformat(raw)}")
		for part in raw.split(","):
			# logger.info(f"VECTOR PART: {pprint.pformat(part)}")
			out.append(parse_number(part))
	return out


def parse_value(raw, do_debug = False):
	if do_debug:
		logger.info(f"parse_value({raw})")
	if raw:
		text = raw.strip()
		m = bool_val_re.match(text)
		if m:
			ret={ "type":"bool", "value": "true" == m.groupdict().get("value", "false").strip().lower()}
			if do_debug:
				logger.info(f"MATCHED BOOL: {pprint.pformat(ret)}")
			return  ret
		m = string_val_re.match(text)
		if m:
			ret = { "type":"string", "value": m.groupdict().get("value", "")}
			if do_debug:
				logger.info(f"MATCHED STRING: {pprint.pformat(ret)}")
			return  ret
		m = number_val_re.match(text)
		if m:
			ret = { "type":"number", "value": parse_number(m.groupdict().get("value", 0))}
			if do_debug:
				logger.info(f"MATCHED NUMBER: {pprint.pformat(ret)}")
			return  ret
		m = vector_val_re.match(text)
		if m:
			# logger.info("------------------")
			# pprint.pformat(m.groupdict())
			# logger.info("------------------")
			v = m.groupdict().get("value")
			# logger.info(f"BALLLLLLS {v}")
			ret = { "type":"vector", "value": parse_vector(v)}
			if do_debug:
				logger.info(f"MATCHED VECTOR: {pprint.pformat(ret)}")
			return  ret
	else:
		logger.warn(f"NO RAW '{raw}'")
	if do_debug:
		logger.info(f"NO MATCH FOR {raw}")
	return dict()


def parse_range_schema(text, do_debug = False):
	if do_debug:
		logger.info(" parse_range_schema()")
	ret = {"raw":text}
	m = range1_schema_re.match(text) or range2_schema_re.match(text) or range3_schema_re.match(text)
	if m:
		g = m.groupdict()
		if do_debug:
			logger.info(f"   + range {g}")
		ret["min"] = parse_number(g.get("min"))
		ret["step"] = parse_number(g.get("step"))
		ret["max"] = parse_number(g.get("max"))
		ret["unit"] = str(g.get("unit"))
		if do_debug:
			logger.info(f"   + range {ret['min']}, {ret['step']}, {ret['max']}:")
	return ret


def parse_number_values_schema(text, do_debug = False):
	# logger.info(" parse_number_values_schema()")
	ret = {"raw":text}
	# Labels
	m = labeled_number_schema_re.match(text)
	if m:
		g = m.groupdict()
		#logger.info(f"   + values {g}")
		vs = g.get("values")
		if vs:
			labels = dict()
			for pair in [ v.strip().split(":") for v in vs.split(",")]:
				labels[parse_number(pair[0])] = pair[1]
			ret["labels"] = labels
		else:
			#logger.info(f"   + vs {pprint.pformat(vs)}")
			pass
		# logger.info(f"   + string {pprint.pformat(ret)}")
	else:
		# Values
		m = values_number_schema_re.match(text)
		if m:
			g = m.groupdict()
			#logger.info(f"   + values {g}")
			vs = g.get("values")
			if vs:
				ret["values"] = [ parse_number(v) for v in vs.split(",")]
			else:
				#logger.info(f"   + vs {pprint.pformat(vs)}")
				pass
			# logger.info(f"   + string {pprint.pformat(ret)}")
		else:
			logger.warning(f"Problem parsing values for: {text}")
	return ret

def parse_number_schema(text):
	# logger.info(" parse_number_schema()")
	ret = parse_range_schema(text)
	if not ret.get("max"):
		# logger.warning(f"No range found, trying values for '{text}'")
		ret = parse_number_values_schema(text)
	return ret

def parse_vector_schema(text):
	# logger.info(" parse_vector_schema()")
	return parse_range_schema(text)

def parse_string_schema(text):
	# logger.info(" parse_string_schema()")
	ret = {"raw":text}
	# Labels
	m = labeled_string_schema_re.match(text)
	if m:
		g = m.groupdict()
		#logger.info(f"   + values {g}")
		vs = g.get("values")
		if vs:
			labels = dict()
			for pair in [ v.strip().split(":") for v in vs.split(",")]:
				labels[pair[0]] = pair[1]
			ret["labels"] = labels
		else:
			#logger.info(f"   + vs {pprint.pformat(vs)}")
			pass
		# logger.info(f"   + string {pprint.pformat(ret)}")
	else:
		# Values
		m = values_string_schema_re.match(text)
		if m:
			g = m.groupdict()
			#logger.info(f"   + values {g}")
			vs = g.get("values")
			if vs:
				ret["values"] = [ v.strip() for v in vs.split(",")]
			else:
				#logger.info(f"   + vs {pprint.pformat(vs)}")
				pass
			# logger.info(f"   + string {pprint.pformat(ret)}")
	return ret

def parse_bool_schema(text):
	# logger.info(" parse_bool_schema()")
	ret = {"raw":text}
	# Labels
	m = labeled_bool_schema_re.match(text)
	if m:
		g = m.groupdict()
		#logger.info(f"   + values {g}")
		vs = g.get("values")
		if vs:
			labels = dict()
			for pair in [ v.strip().split(":") for v in vs.split(",")]:
				labels[pair[0]] = pair[1]
			ret["labels"] = labels
		else:
			#logger.info(f"   + vs {pprint.pformat(vs)}")
			pass
		# logger.info(f"   + string {pprint.pformat(ret)}")
	return ret


def parse_schema(raw, type):
	# logger.info(" parse_schema()")
	if raw:
		#logger.info(f"RAW {raw}:")
		text = raw.strip()
		if type == "number":
			return parse_number_schema(text)
		elif type == "vector":
			return parse_vector_schema(text)
		elif type == "string":
			return parse_string_schema(text)
		elif type == "bool":
			return parse_bool_schema(text)
		return {"debug":f"NO SCHEMA FOR {raw} with type '{type}'"}
	else:
		return {"debug":f"NO RAW {raw} with type '{type}'"}

def parse_customize(source, do_debug = False):
	#logger.info(" parse_customize()")
	source = str(source)
	lines = source.split("\n")
	last_h1 = None
	last_h2 = None
	last_unit = None
	parameters_list = list()
	start = now()
	for line in lines:
		line=line.strip()
		if line =="":
			continue
		if do_debug:
			logger.info("======================================")
		t = "?"
		if line.startswith("$"):
			t="$"
		m = var_re.match(line)
		if m:
			t = "VAR"
			g = m.groupdict()
			variable = g.get('variable')
			value = g.get('value')
			default = parse_value(value, do_debug = do_debug)
			type = default.get("type")
			comment = g.get('comment')
			schema = parse_schema(comment, type)
			# Clean up
			variable = variable and variable.strip()
			value = value and value.strip()
			default_value = default.get("value")
			# Make sure that values contain the default value for consistency
			values = schema and schema.get("values")
			if values:
				if None != default_value and not default_value in values:
					values.append(default_value)
					schema["values"] = values
			# Make sure that labels contain the default value for consistency
			labels = schema and schema.get("labels")
			if labels:
				if None != default_value and not default_value in labels:
					labels[default_value] = "default"
					schema["labels"] = labels
				label = labels.get(default_value)
				#schema["label"] = label
			var = {
				  "name": variable
				, "description": last_h2 and last_h2.strip()
				, "section": last_h1 and last_h1.strip()
				, "default": default
				, "unit": last_unit
				, "schema": schema
			}
			parameters_list.append(var)
			# Avoid re-using unit and section
			last_unit = None
			last_h2 = None
		else:
			m = h2_re.match(line)
			if m:
				g = m.groupdict()
				t=" H2"
				last_h2 = g.get("description")
				last_unit = g.get("unit")
			else:
				m = h1_re.match(line)
				if m:
					t=" H1"
					g = m.groupdict()
					name = g.get("section")
					last_h1 = name and name.strip()
				else:
					pass
					#break;
		if do_debug:
			logger.info(f"{t}: {line}")
		if "?" == t:
			# End of initial variable section
			break;
	took = now() - start
	if do_debug:
		logger.info("#"*240)
		logger.info("\n"*2)
	#logger.info(f"Parsing took {octomy.utils.human_delta(took)}")
	#logger.info(f"Final parsed parameters for source {octomy.utils.human_bytesize(len(source))} ({len(lines)} lines):")
	#logger.info(f"parameters:{len(parameters_list)}")
	#logger.info(f"D:{pprint.pformat(parameters_list)}")
	#logger.info("...")
	return parameters_list


class RenderMode(Enum):
	"""
	RenderMode Enum class.
	- test_only
	- render
	- preview
	- thrown_together
	- wireframe
	"""
	test_only = "Test"
	render = "Render"
	preview = "Preview"
	thrown_together = "Thrown Together"
	wireframe = "Wireframe"


class ColorScheme(Enum):
	"""
	ColorScheme Enum class.
	- cornfield
	- metallic
	- sunset
	- starnight
	- beforedawn
	- nature
	- deepocean
	- solarized
	- tomorrow
	- tomorrow_night
	- monotone
	"""
	cornfield      = "Cornfield"
	metallic       = "Metallic"
	sunset         = "Sunset"
	starnight      = "Starnight"
	beforedawn     = "BeforeDawn"
	nature         = "Nature"
	deepocean      = "DeepOcean"
	solarized      = "Solarized"
	tomorrow       = "Tomorrow"
	tomorrow_night = "Tomorrow Night"
	monotone       = "Monotone"

# From https://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def which(program):
	def is_exe(fpath):
		return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

	fpath, fname = os.path.split(program)
	if fpath:
		if is_exe(program):
			return program
	else:
		for path in os.environ.get("PATH", "").split(os.pathsep):
			exe_file = os.path.join(path, program)
			if is_exe(exe_file):
				return exe_file

	return None

class OpenScadRunner(object):
	def __init__(
		  self
		, scriptfile
		, outfiles
		, version = False
		, animate = None
		, animate_duration = 250
		, antialias = 1.0
		, auto_center = False
		, camera = None
		, color_scheme = ColorScheme.cornfield
		, csg_limit = None
		, customizer_file = None
		, customizer_params = dict()
		, customizer_sets = list()
		, deps_file = None
		, hard_warnings = False
		, imgsize = (1024, 1024)
		, make_file = None
		, orthographic = False
		, quiet = False
		, render_mode = RenderMode.render
		, set_vars = dict()
		, show_axes = True
		, show_crosshairs = False
		, show_edges = False
		, show_scales = True
		, verbose = False
		, view_all = False
		):
		
		"""
		Initializer method.  Arguments are:
		- scriptfile = The name of the script file to process.
		- outfiles = A list of output files to produce. The filetype  for each file is deduced by the extensions.
		- version = If enabled, the program will return version as a string and quit, ignoring all other parameters
		- animate = If given an integer number of frames, creates that many frames of animation, and collates them into an animated GIF.  Default: None
		- animate_duration = Number of milliseconds per frame for an animated GIF.  Default: 250
		- antialias = The antialiasing scaling factor.  If greater than 1.0, images are generated at a larger size, then scaled down to the target size with anti-aliasing.  Default: 1.0  (no anti-aliasing)
		- auto_center = If True, and script does not set $vpt, $vpr, or $vpd, then centers the shape in the rendered image.  Default: False
		- camera = Gives the camera position as either [translate_x,y,z,rot_x,y,z,dist] or [eye_x,y,z,center_x,y,z]
		- color_scheme = The color scheme to render an image with.  See ColorScheme Enum.  Default: ColorScheme.cornfield,
		- csg_limit = If given, the maximum number of CSG elements to render.
		- customizer_file = If given, specifies the file containing Customizer Parameters.
		- customizer_params = An optional list of parameter to set directly
		- customizer_sets = A list of the parameter sets taht should be used from customizer_file.
		- deps_file = If given, the file to write Makefile dependancies out to.
		- hard_warnings = Stop at first WARNING, as if it were an ERROR.  Default: False
		- imgsize = The size of the imagefile to output to, if outputting to a PNG or GIF.  Default: (640,480)
		- make_file = If given, the Makefile script to run when missing a dependency.
		- orthographic = If True, render orthographic.  If False, render with perspective.  Default: False
		- predefined_variables = An optional set of variables to set
		- quiet = Suppresses non-error, non-warning messages.  Default: False
		- render_mode = The rendering mode to use when generating an image.  See RenderMode Enum.  Default: RenderMode.render
		- set_vars = An optional dictionary of script variables and values to set.
		- show_axes = If True, show axes in the rendering.  Default: True
		- show_crosshairs = If True, shows the crosshairs for the center of the camera translation.  Default: False
		- show_edges = If True, shows the edges of all the faces.  Default: False
		- show_scales = If True, show the scales along the axes.  Default: True
		- verbose = Print the command-line to stdout on each execution.  Default: False
		- view_all = If True, and script does not set $vpd, then the field of view is scaled to show the complete rendered shape.  Default: False
		"""
		self.command = "/usr/bin/openscad"
		self.scriptfile = scriptfile
		self.outfiles = outfiles
		self.version = version
		self.animate = animate
		self.animate_duration = animate_duration
		self.antialias = antialias
		self.auto_center = auto_center
		self.camera = camera
		self.color_scheme = color_scheme
		self.csg_limit = csg_limit
		self.customizer_file = customizer_file
		self.customizer_params = customizer_params
		self.customizer_sets = customizer_sets
		self.deps_file = deps_file
		self.hard_warnings = hard_warnings
		self.imgsize = imgsize
		self.make_file = make_file
		self.orthographic = orthographic
		self.quiet = quiet
		self.render_mode = render_mode
		self.set_vars = set_vars
		self.show_axes = show_axes
		self.show_crosshairs = show_crosshairs
		self.show_edges = show_edges
		self.show_scales = show_scales
		self.summary = "all"
		self.verbose = verbose
		self.view_all = view_all
		self.timeout = 2*60
		self.reset()

	def reset(self):
		self.cmdline = []
		self.complete = False
		self.echos = []
		self.errors = []
		self.return_code = None
		self.script = []
		self.stderr = []
		self.stdout = []
		self.success = False
		self.warnings = []

	def __bool__(self):
		"""
		Returns True if the run() method has been called, and the processing is complete, whether or not it was successful.
		"""
		return self.complete

	def good(self):
		"""
		Returns True if the run() method has been called, and the result was successful.
		"""
		return self.success

	def _process_frame(self, imgfile):
		img = Image.open(imgfile)
		img.thumbnail(self.imgsize, Image.ANTIALIAS)
		os.unlink(imgfile)
		img.save(imgfile)
		
	def _process_animation(self, basename):
		imgfiles = ["{}{:05d}.png".format(basename,i) for i in range(self.animate)]
		if fileext == ".gif":
			imgs = []
			for imgfile in imgfiles:
				img = Image.open(imgfile)
				if self.antialias != 1.0:
					img.thumbnail(self.imgsize, Image.ANTIALIAS)
				imgs.append(img)
			imgs[0].save(
				self.outfile,
				save_all=True,
				append_images=imgs[1:],
				duration=self.animate_duration,
				loop=0
			)
			pygifsicle.optimize(self.outfile, colors=64)
		elif fileext == ".png":
			if self.antialias != 1.0:
				for imgfile in imgfiles:
					self._process_frame(imgfile)
			APNG.from_files(imgfiles, delay=self.animate_duration).save(self.outfile)
		for imgfile in imgfiles:
			os.unlink(imgfile)

	def _check_command_availability(self):
		w = which(self.command)
		return w and True or False

	def _prepare_cmd(self):
		self.foo_file = "foo.term"
		outfiles = self.outfiles
		"""
		basename, fileext = os.path.splitext(outfile)
		fileext = fileext.lower()
		if self.animate is not None:
			assert (fileext in (".gif", ".png")), "Can only animate to a gif or png file."
			basename = basename.replace(".", "_")
			outfile = basename + ".png"
		"""
		self.command_line = list()
		if self.version:
			self.command_line = [self.command, "--version"]
			return
		if self.animate is not None:
			logger.error("Animation not supported at this time, aborting...")
			return None

		if self.render_mode == RenderMode.test_only:
			self.command_line = [self.command, "-o", self.foo_file]
		else:
			self.command_line = [self.command]
			if isinstance(outfiles, str):
				outfiles = [ outfiles]
			if type(outfiles) is not list:
				logger.error("Malformed outfiles: {pprint.pformat(outfiles)}")
				return None
			for outfile in outfiles:
				self.command_line.extend(["-o", shex(outfile)])
			"""
			if fileext in [".png", ".gif"]:
				self.command_line.append(f"--imgsize={int(self.imgsize[0] * self.antialias)},{int(self.imgsize[1] * self.antialias)}")
			"""
			if self.imgsize:
				#self.command_line.append(f"--imgsize={int(self.imgsize[0] * self.antialias)},{int(self.imgsize[1] * self.antialias)}")
				self.command_line.extend(["--imgsize", f"{int(self.imgsize[0] * self.antialias)},{int(self.imgsize[1] * self.antialias)}"])
			if self.show_axes or self.show_scales or self.show_edges or self.show_crosshairs or self.render_mode==RenderMode.wireframe:
				showparts = []
				if self.show_axes:
					showparts.append("axes")
				if self.show_scales:
					showparts.append("scales")
				if self.show_edges:
					showparts.append("edges")
				if self.show_crosshairs:
					showparts.append("crosshairs")
				if self.render_mode == RenderMode.wireframe:
					showparts.append("wireframe")
				self.command_line.append("--view=" + ",".join(showparts))
			if self.camera is not None:
				while len(self.camera) < 6:
					self.camera.append(0)
				self.command_line.extend(["--camera", ",".join(str(x) for x in self.camera)])
			if self.color_scheme != ColorScheme.cornfield:
				self.command_line.extend(["--colorscheme", self.color_scheme])
			self.command_line.append("--projection=o" if self.orthographic else "--projection=p")
			if self.auto_center:
				self.command_line.append("--autocenter")
			if self.view_all:
				self.command_line.append("--viewall")
			if self.animate is not None:
				self.command_line.extend(["--animate", str(self.animate)])
			if self.render_mode == RenderMode.render:
				self.command_line.extend(["--render", ""])
			elif self.render_mode == RenderMode.preview:
				self.command_line.extend(["--preview", ""])
			elif self.render_mode == RenderMode.thrown_together:
				self.command_line.extend(["--preview", "throwntogether"])
			elif self.render_mode == RenderMode.wireframe:
				self.command_line.extend(["--render", ""])
			if self.csg_limit is not None:
				self.command_line.extend(["--csglimit", self.csg_limit])
		if self.deps_file != None:
			self.command_line.extend(["-d", self.deps_file])
		if self.summary:
			pass #self.command_line.extend(["--summary", self.summary])
		# https://ochafik.com/jekyll/update/2022/02/09/openscad-fast-csg-contibution.html
		#self.command_line.extend(["--enable", "lazy-union"])
		#self.command_line.extend(["--enable", "fast-csg"])
		if self.make_file != None:
			self.command_line.extend(["-m", self.make_file])
		for var, val in self.set_vars.items():
			self.command_line.extend(["-D", f"{var}={val}"])
		if self.customizer_file is not None:
			self.command_line.extend(["-p", shex(self.customizer_file)])
		for var, val in self.customizer_params.items():
			self.command_line.extend(["-D", f"{shex(var)}={shex(val)}"])
		for setName in self.customizer_sets:
			self.command_line.extend(["-P", f"{shex(setName)}"])
		if self.hard_warnings:
			self.command_line.append("--hardwarnings")
		if self.quiet:
			self.command_line.append("--quiet")
		self.command_line.append(shex(self.scriptfile))
		if self.verbose:
			line = " ".join([
				f"'{arg}'" if ' ' in arg or arg == '' else arg
				for arg in self.command_line
			])
			logger.info("Commandline:")
			logger.info(line)

	def to_string(self):
		pass

	def error_string(self):
		return "\nERR:".join(self.errors) + "\nWARN:".join(self.warnings)+ "\nSTDERR:".join(self.stderr)+ "\nCMD:".join(self.command_line)


	async def _async_run(self):
		# https://docs.python.org/3/library/asyncio-subprocess.html#examples
		# coroutine asyncio.create_subprocess_exec(
		#	program
		#	, *args
		#	, stdin=None
		#	, stdout=None
		#	, stderr=None
		#	, limit=None
		#	, **kwds)

		args = list(self.command_line)
		program = args.pop()
		logger.info("Program: {program}")
		logger.info("Args: {len(args)}")
		proc = await asyncio.create_subprocess_exec(
			program = program
			, args = args
			, stdin = asyncio.subprocess.PIPE
			, stdout = asyncio.subprocess.PIPE
			, stderr = asyncio.subprocess.PIPE
			, close_fds = True)
	
		# Read one line of output.
		data = await proc.stdout.readline()
		line = data.decode('ascii').rstrip()
	
		# Wait for the subprocess exit.
		await proc.wait()
		return line
	
		date = asyncio.run(get_date())
		print(f"Current date: {date}")
		

	def _sync_run(self):
		try:
			proc = subprocess.Popen(self.command_line, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
			(stdoutdata, stderrdata) = proc.communicate(timeout=self.timeout)
			return stdoutdata, stderrdata, proc.returncode
		except subprocess.TimeoutExpired as te:
			logger.error(f"Command timed out after {self.timeout} seconds")
			return b"", b"", -1

	def run(self):
		"""
		Runs the OpenSCAD application with the current paramaters.
		"""
		try:
			start = now()
			self.reset()
			if not self._check_command_availability():
				self.errors = [f"Command not found or not executable ('{self.command}') "]
				self.success = False
				return self.success, self.error_string()
			self._prepare_cmd()
			stdoutdata = ""
			stderrdata = ""
			returncode = None
			self.do_async = False
			if self.do_async:
				stdoutdata, stderrdata, returncode = self._async_run()
			else:
				stdoutdata, stderrdata, returncode = self._sync_run()
			stdoutdata = stdoutdata.decode('utf-8')
			stderrdata = stderrdata.decode('utf-8')
			if self.verbose:
				logger.info("RAW STDOUT:")
				logger.info(stdoutdata)
				logger.info("RAW STDERR:")
				logger.info(stderrdata)
			self.return_code = returncode
			self.cmdline = self.command_line
			self.stderr = stderrdata.split("\n")
			self.stdout = stdoutdata.split("\n")
			self.echos    = [x for x in self.stderr if x.startswith("ECHO:")]
			self.warnings = [x for x in self.stderr if x.startswith("WARNING:")]
			self.errors   = [x for x in self.stderr if x.startswith("ERROR:") or x.startswith("TRACE:")]
			if self.version:
				self.version = parse_version(stderrdata)
				logger.info(f"PARSED VERSION: {stderrdata} into {self.version}")
			# OLD SUCCESS:
			"""
			if self.return_code == 0 and self.errors == [] and (not self.hard_warnings or self.warnings == []):
				self.success = True
			"""
			if self.return_code == 0:
				self.success = True
			if self.render_mode == RenderMode.test_only and os.path.isfile(self.foo_file):
				os.unlink(self.foo_file)
			#with open(self.scriptfile, "r") as f:
			#	self.script = f.readlines();
			if self.success and self.render_mode != RenderMode.test_only:
				if not self.animate:
					if float(self.antialias) != 1.0:
						for outfile in self.outfiles:
							self._process_frame(outfile)
				else:
					self.process_animation(basename)
			self.complete = True
			took = now() - start
			logger.info(f"Rendering took {octomy.utils.human_delta(took)}")
			return self.success, self.success and None or self.error_string()
		except Exception as e:
			logger.exception("Error occurred while running OpenScad")
			return self.success, f"Exception: '{pprint.pformat(e)}'"
		# Whatever happened here, tell the system
		return self.success, "Unexpected end of run()"
