from octomy import utils
from octomy.cad import openscad
from octomy.cad.generators import file_properties
from octomy.cad.types import *
import datetime
import jinja2
import json
import logging
import os
import pprint
import random
import re

logger = logging.getLogger(__name__)


def to_openscad_parameters(parameters:GeneratorParameters, set_name = "set", do_debug = False):
	out = dict()
	for p in parameters.parameters:
		out[p.name] = p.value
	out = {
		"fileFormatVersion": "1"
		, "parameterSets": {
			set_name: out
		}
	}
	if do_debug:
		logger.info("parameters in openscad format:")
		logger.info(pprint.pformat(out))
	return out


def millinow():
	tz = datetime.timezone.utc
	now = datetime.datetime.now(tz)
	epoch = datetime.datetime(1970, 1, 1, tzinfo = tz) # use POSIX epoch
	posix_timestamp_millis = (now - epoch) // datetime.timedelta(milliseconds = 1) 
	return posix_timestamp_millis


def generate_local_temp_names(id):
	# Add millisecond timestamp to avoid problems in the (rare) case where two calls are made for the same file at the same time
	now = millinow()
	local_name_base = f"{id}_{now}"
	local_name_model = f"/tmp/{local_name_base}.openscad"
	local_name_stl = f"/tmp/{local_name_base}.stl"
	local_name_json = f"/tmp/{local_name_base}.json"
	local_name_log = f"/tmp/{local_name_base}.log"
	local_name_png = f"/tmp/{local_name_base}.png"
	return now, local_name_base, local_name_model, local_name_stl, local_name_json, local_name_log, local_name_png

def generate_derivative_filenames(id, parameters):
	if not parameters:
		logger.warning(f"No parameters ({parameters}) provided while generating derivative filenames for '{id}'")
		return None, None, None, None, None, None
	key = utils.calculate_unique_key(parameters.json())
	drive_name_base = f"{id}_{key}"
	drive_name_stl = f"{drive_name_base}.stl"
	drive_name_json = f"{drive_name_base}.json"
	drive_name_png = f"{drive_name_base}.png"
	drive_name_log = f"{drive_name_base}.log"
	return key, drive_name_base, drive_name_stl, drive_name_json, drive_name_png, drive_name_log


def _prepare_log(cmdline, stdout, stderr, returncode):
	cmdline = " \\\n\t".join(cmdline)
	stdout = "\n".join(stdout)
	stderr = "\n".join(stderr)
	return f"""
---
title: commandline
returncode: {returncode}
---		
{cmdline}

---
title: stdout
---
{stdout}

---
title: stderr
---
{stderr}


	"""

class OpenSCADGenerator:
	def __init__(self, common):
		self.common = common
		self.version = None
		
	def _get_version_worker(self):
		openscad_parameters = {
			"version": True
		}
		oscad = openscad.OpenScadRunner(
			scriptfile = None
			, outfiles = None
			, **openscad_parameters)
		ok, err = oscad.run()
		if ok:
			return oscad.version
		else:
			logger.warning(f"Could not get version: {err}")
		return None

	def get_version(self) -> str:
		if not self.version:
			self.version = self._get_version_worker()
		return self.version and str(self.version) or None
		

	def get_schema(self, source, do_debug = False):
		#logger.info(f"PARSING SCHEMA FROM SOURCE: '{source}':")
		schema = openscad.parse_customize(source = source, do_debug = do_debug)
		#logger.info(pprint.pformat(schema))
		return schema


	def generate(self, source_name, source, parameters, id, do_stl=True, do_png=True, do_debug = False):
		set_name = "set"
		image_sz = 1600;
		openscad_parameters = to_openscad_parameters(parameters, set_name)
		json_parameters = json.dumps(openscad_parameters, indent=3)
		now, local_name_base, local_name_model, local_name_stl, local_name_json, local_name_log, local_name_png = generate_local_temp_names(id)
		key, drive_name_base, drive_name_stl, drive_name_json, drive_name_png, drive_name_log = generate_derivative_filenames(id, parameters)
		with open(local_name_json, "w") as f:
			f.write(json_parameters)
		openscad_parameters = {
			  "animate": None
			, "animate_duration": 250
			, "antialias": 1.0
			, "auto_center": True
			, "camera": None
			, "color_scheme": openscad.ColorScheme.cornfield
			, "csg_limit": None
			, "customizer_file": local_name_json
			, "customizer_params": dict()
			, "customizer_sets": [set_name]
			, "deps_file": None
			, "hard_warnings": False
			, "imgsize": (1600,1600)
			, "make_file": None
			, "orthographic": False
			, "quiet": False
			, "render_mode": openscad.RenderMode.render
			, "set_vars": dict()
			, "show_axes": True
			, "show_crosshairs": False
			, "show_edges": False
			, "show_scales": True
			, "verbose": do_debug or True
			, "view_all": True
		}
		outfiles = list()
		stl_file_id = None
		json_file_id = None
		log_file_id = None
		png_file_id = None

		with open(local_name_model, "wb") as f:
			f.write(source)
		source_folder_id = self.common.ensure_source_folder(source_name)
		part_folder_id = self.common.ensure_part_folder(source_folder_id, key)
	
		if do_stl:
			outfiles.append(local_name_stl)
		if do_png:
			outfiles.append(local_name_png)
		if len(outfiles) > 0:
			oscad = openscad.OpenScadRunner(
				scriptfile = local_name_model
				, outfiles = outfiles
				, **openscad_parameters)
			ok, err = oscad.run()
			if ok:
				props = file_properties(id, key)
				log = _prepare_log(oscad.cmdline, oscad.stdout, oscad.stderr, oscad.return_code)
				with open(local_name_log, "w") as f:
					f.write(log)
				if do_stl:
					stl_file_id = self.common.upload_derivative(local_name_stl, part_folder_id, drive_name_stl, MIMETYPE_STL_MODEL, props)
					json_file_id = self.common.upload_derivative(local_name_json, part_folder_id, drive_name_json, MIMETYPE_JSON_DATA, props)
					log_file_id = self.common.upload_derivative(local_name_log, part_folder_id, drive_name_log, MIMETYPE_TEXT, props)
				if do_png:
					png_file_id = self.common.upload_derivative(local_name_png, part_folder_id, drive_name_png, MIMETYPE_PNG_IMAGE, props)
					if stl_file_id:
						self.common.set_drive_thumbnail_from_local_path(stl_file_id, local_name_png)
			else:
				logger.warning("The parameters were:")
				logger.warning(json_parameters)
				logger.error(f"ERROR(S) OCCURRED for oscad run: {err}")
				utils.delete_file(local_name_json)
				utils.delete_file(local_name_stl)
				utils.delete_file(local_name_model)
				return None, {"message":"Could not generate stl from source with OpenSCAD", "error": oscad.error_string()}
		# Clean up local temp files
		utils.delete_file(local_name_json)
		utils.delete_file(local_name_model)
		utils.delete_file(local_name_png)
		utils.delete_file(local_name_stl)
		if do_debug:
			logger.info(f"Returning: {stl_file_id}")
		return {
			  "model_id": stl_file_id
			, "parameters_id": json_file_id
			, "log_id": log_file_id
			, "thumbnail_id": png_file_id
		}, None
