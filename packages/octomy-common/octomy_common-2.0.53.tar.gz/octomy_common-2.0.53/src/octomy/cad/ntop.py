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


logger = logging.getLogger(__name__)



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

class NTopRunner(object):
	def __init__(
		  self
		, scriptfile
		, outfiles
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
		self.command = "/usr/bin/ntop"
		self.scriptfile = scriptfile
		self.outfiles = outfiles
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
				logger.error("Malforemd outfiles: {pprint.pformat(outfiles)}")
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
		# https://ochafik.com/jekyll/update/2022/02/09/ntop-fast-csg-contibution.html
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
		Runs the ntop application with the current paramaters.
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
			# OLD SUCCESS:
			"""
			if self.return_code == 0 and self.errors == [] and (not self.hard_warnings or self.warnings == []):
				self.success = True
			"""
			if self.return_code == 0:
				self.success = True
			if self.render_mode == RenderMode.test_only and os.path.isfile(self.foo_file):
				os.unlink(self.foo_file)
			with open(self.scriptfile, "r") as f:
				self.script = f.readlines();
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
			logger.exception("Error occurred while running ntop")
			return self.success, f"Exception: '{pprint.pformat(e)}'"
		# Whatever happened here, tell the system
		return self.success, "Unexpected end of run()"
