 #!/bin/env python3
from octomy import utils
from octomy.cad.generators import generators_map, common, file_properties, oktopus_folder_name
from octomy.cad.types import *
from octomy.storage.google_drive import GoogleDrive, FOLDER_MIMETYPE, folder_id as google_drive_folder_id
from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional, Union
import base64
import datetime
import jinja2
import logging
import math
import os
import pathlib
import pprint
import random
import re
import time


logger = logging.getLogger(__name__)


DEFAULT_UNIT = "mm"

MIN_UPDATE_FREQ = 1000 * 60 # Update at least every minute

# Dir where data is kept
data_dir = "data"

# Maximum filesize allowed
data_file_max_size = 1024*1024*1024*2 # 2 GiB



# Number of floats per record (bar) of data
data_float_bytes = 4
#open: float
#high: float
#low: float
#close: float
#volume: float
#trade_count: Optional[float]
#vwap: Optional[float]
#pad: float #8 x float alignment padding

# Number of bytes per float
data_columns = 8

# Maximum number onf indices per file
data_file_max_index = data_file_max_size / (data_columns * data_float_bytes)


parts_by_id = dict()


model_format_map = {
	  MIMETYPE_OPENSCAD_MODEL: "OpenSCAD"
	, MIMETYPE_NTOP_MODEL: "nTop"
}

def understand_model_format(mimetype):
	if not mimetype:
		return False, "Unknown"


def millinow():
	tz = datetime.timezone.utc
	now = datetime.datetime.now(tz)
	epoch = datetime.datetime(1970, 1, 1, tzinfo = tz) # use POSIX epoch
	posix_timestamp_millis = (now - epoch) // datetime.timedelta(milliseconds = 1) 
	return posix_timestamp_millis



##################################################################


def calculate_filenames(id, parameters, model_type="scad", output_type="stl"):
	# Add millisecond timestamp to avoid problems in the (rare) case where two calls are made for the same file at the same time
	now = millinow()
	local_name_base = f"/tmp/{id}_{now}/part"
	local_name_input = f"{local_name_base}.{model_type}"
	local_name_output = f"{local_name_base}.{output_type}"
	local_name_meta = f"{local_name_base}.json"
	local_name_log = f"{local_name_base}.log"
	local_name_thumbnail = f"{local_name_base}.png"
	key = utils.calculate_unique_key(parameters.json())
	storage_name_base = f"{id}_{key}"
	storage_name_output = f"{storage_name_base}.{output_type}"
	storage_name_meta = f"{storage_name_base}.json"
	storage_name_log = f"{storage_name_base}.log"
	storage_name_thumbnail = f"{storage_name_base}.png"
	return {
		  "key": key
		, "now": now
		, "local_name_base": local_name_base
		, "local_name_input": local_name_input
		, "local_name_output": local_name_output
		, "local_name_meta": local_name_meta
		, "local_name_log": local_name_log
		, "local_name_thumbnail": local_name_thumbnail
		, "storage_name_base": storage_name_base
		, "storage_name_output": storage_name_output
		, "storage_name_meta": storage_name_meta
		, "storage_name_log": storage_name_log
		, "storage_name_thumbnail": storage_name_thumbnail
	}

def prepare_gen_job(part_id, part_folder_id):
	return {
		  "part_id": part_id
		, "parameters": parameters
		, "part_folder_id": part_folder_id
		, "storage_name_base": storage_name_base
		, "storage_name_output": storage_name_output
		, "storage_name_meta": storage_name_meta
		, "storage_name_log": storage_name_log
		, "storage_name_thumbnail": storage_name_thumbnail
	}

def determine_file_extension(file_path: str):
	if not file_path:
		return None, "No file path"
	index = file_path.rfind(".")
	if index < 0:
		return None, "No file extention separator"
	file_ending = file_path[index + 1 :]
	if not file_ending:
		return None, "No file extention"
	return file_ending, None

def file_extension_is_binary(ext):
	return not ext in ["md", "htm", "html", "inc", "txt", "svg", "csv", "json", "jinja2", "jinja", "j2", "tpl", "scad"]

def file_is_binary(path):
	ext, err = determine_file_extension(path)
	if ext:
		return file_extension_is_binary(ext)
	# Fall back to binary to be safe
	return True


def properties_to_query(properties):
	if not properties:
		return ""
	all = list()
	for key, value in properties.items():
		all.append(f"properties has {{ key='{key}' and value='{value}' }}")
	return "and ".join(all)

def pretty_name(basename):
	return os.path.splitext(basename)[0];

##################################################################


def convert_schema(schemas, version = None, do_debug = False):
	output_schema = list()
	for input_parameter in schemas:
		output_parameter = None
		if do_debug:
			logger.info(f"input_parameter:\n{pprint.pformat(input_parameter)}")
		default = input_parameter.get("default", dict())
		if not default:
			logger.warning(f"No default for {pprint.pformat(input_parameter)}, skipping parameter")
			continue
		_type = default.get("type")
		if not _type:
			logger.warning(f"No type for {pprint.pformat(input_parameter)}, skipping parameter")
			continue
		section = input_parameter.get("section")
		if not section:
			if do_debug:
				logger.warning(f"No section for {pprint.pformat(input_parameter)}, skipping parameter")
			continue
		schema = input_parameter.get("schema", dict())
		name = input_parameter.get("name")
		default_unit = input_parameter.get("unit")
		default_value = default.get("value")
		description = input_parameter.get("description")
		if _type == "number":
			if schema:
				if schema.get("labels"):
					if do_debug:
						logger.info(f"Adding numeric labels parameter {name} ({pprint.pformat(schema)})")
					labels = list()
					for label_value, label_name in schema.get("labels").items():
						if do_debug:
							logger.info(f"  + {label_name}={label_value}({type(label_value)})")
						labels.append(NumericLabelGeneratorParameterValue(name=str(label_name), value=label_value))
					output_parameter = NumericLabelGeneratorParameterSchema(
						  name = name
						, labels = labels
						, default = default_value
						, unit = default_unit
						, description = description
						, section = section)
				elif schema.get("values"):
					if do_debug:
						logger.info(f"Adding numeric values parameter {name} ({pprint.pformat(schema)})")
					labels = list()
					for label_value in schema.get("values"):
						#logger.info(f"  + value={label_value}")
						labels.append(NumericLabelGeneratorParameterValue(name=str(label_value), value=label_value))
					output_parameter = NumericLabelGeneratorParameterSchema(
						  name = name
						, labels = labels
						, default = default_value
						, unit = default_unit
						, description = description
						, section = section)
				else:
					#logger.info(f"Adding numeric range parameter {name} ({pprint.pformat(schema)})")
					output_parameter = NumericRangeGeneratorParameterSchema(
						  name = name
						, min = schema.get("min")
						, step = schema.get("step")
						, max = schema.get("max")
						, default = default_value
						, unit = default_unit
						, description = description
						, section = section)
		elif _type == "string":
			if schema.get("labels"):
				if do_debug:
					logger.info(f"Adding string labels parameter '{name}' ({pprint.pformat(schema)})")
				labels = list()
				for label_value, label_name in schema.get("labels").items():
					logger.info(f"  + {label_name}={label_value}")
					labels.append(StringLabelGeneratorParameterValue(name=label_name, value=label_value))
				output_parameter = StringLabelGeneratorParameterSchema(
					  name = name
					, labels = labels
					, default = default_value
					, description = description
					, section = section)
			elif schema.get("values"):
				if do_debug:
					logger.info(f"Adding string values parameter '{name}' ({pprint.pformat(schema)})")
				labels = list()
				for label_value in schema.get("values"):
					logger.info(f"  + value={label_value}")
					labels.append(StringLabelGeneratorParameterValue(name=label_value, value=label_value))
				output_parameter = StringLabelGeneratorParameterSchema(
					  name = name
					, labels = labels
					, default = default_value
					, description = description
					, section = section)
			else:
				if do_debug:
					logger.info(f"Adding literal string parameter {name} ({pprint.pformat(schema)})")
				output_parameter = StringLiteralGeneratorParameterSchema(
					  name = name
					, default = default_value
					, description = description
					, section = section)
		elif _type == "bool":
			if do_debug:
				logger.info(f"Adding bool parameter {name} {pprint.pformat(schema)}")
			output_parameter = BoolGeneratorParameterSchema(
			  name = name
			, default = default_value
			, description = description
			, section = section)
		if output_parameter:
			#logger.info(f"Appending output parameter: {pprint.pformat(output_parameter)}")
			output_schema.append(output_parameter)
			output_parameter = None
		else:
			logger.warning(f"Could not generate output parameter from:\n{pprint.pformat(input_parameter)}")
	#logger.info("-------------------OUTPUT_schema")
	#logger.info(pprint.pformat(output_schema))
	#logger.info("-------------------OUTPUT_schema")
	generator_meta = GeneratorMeta(generator_type = GeneratorTypeEnum.openscad, version = version)
	schema = GeneratorParametersSchema(generator_meta = generator_meta, parameters = output_schema)
	#logger.info(pprint.pformat(json.loads(    schema.json()           )))
	return schema


##################################################################


class Parts:
	def __init__(self):
		utils.inspectify(self)
		self.oktopus_folder_id = None
		self.storage = GoogleDrive()
		self.common = common
		self.update_files()
		self.default_query_stump = "supportsAllDrives = true and includeItemsFromAllDrives = true and corpora = allDrives"

	def source_exists(self, id:str):
		return self.storage.file_exists(id)

	def source(self, id:str, do_debug = False):
		source = self.storage.download_file(id)
		if do_debug:
			logger.info(f"Got source for {id}: {pprint.pformat(source)}")
		if not source:
			return None, "No source for id"
		try:
			source = str(source, 'utf-8')
		except Exception as e:
			logger.error(f"error converting source to utf-8 string for id: {id}")
			logger.warning(f"The related source was {source}")
			logger.exception(e)
		return source, None

	def source_schema(self, id:str, do_debug = False):
		source, source_err = self.source(id)
		if not source:
			return None, source_err
		
		generator_type = GeneratorTypeEnum.openscad
		generator = generators_map.get(generator_type)
		if not generator:
			return None, f"Unknown or unsupported generator '{generator_type}' selected"
		#logger.info(f"Source was {pprint.pformat(source)}")
		schemas = generator.get_schema(source = source, do_debug = do_debug)
		#schemas = parse_customize(source, do_debug)
		if not schemas:
			return None, "No schema for source"
		#logger.info(f"Found schema for id '{id}': {pprint.pformat(schemas)}")
		version = generator.get_version()
		schema = convert_schema(schemas = schemas, version = version, do_debug = do_debug)
		return schema, None


	def find_complete_part_folder(self, source_name, part_name):
		source_folder_id = self.find_source_folder(source_name)
		part_folder_id = source_folder_id and self.find_part_folder(source_folder_id, part_name)
		return part_folder_id


	def _find_derivative(self, id:str, parameters:GeneratorParameters, mimetype = MIMETYPE_STL_MODEL, do_debug = False):
		if not parameters:
			logger.warning(f"No parameters ({parameters}) provided while finding derivative for '{id}' ({mimetype})")
			return None
		key = utils.calculate_unique_key(parameters.json())
		properties_string = properties_to_query(file_properties(id, key))
		q = f"{properties_string} and trashed = false and mimeType = '{mimetype}'"
		files = self.storage.search_files(q = q, fields=['properties'])
		# logger.info(f"Derivative search for id='{id}', key='{key}', mimetype='{mimetype}' resulted in {pprint.pformat(files)}")
		# File existed, return it's id
		if files and len(files) >= 0:
			ret_id = files[0].get("id")
			if do_debug:
				logger.info(f"Found existing derivative for '{id}' ({mimetype})")
			return ret_id
		return None


	def _get_default_parameters(self, schema, do_debug = False):
		# Use default paramters if noen given
		parameters = list()
		
		#logger.info(f"schema 8=======D ~~~  {pprint.pformat(schema)}")
		for parameter in schema.parameters:
			#logger.info(f" + {parameter.name}: {parameter.default}")
			#parameters.append( NumericGeneratorParameter( name = parameter.name, value = parameter.default))
			out = None
			if parameter:
				if isinstance(parameter, BoolGeneratorParameterSchema):
					out = BoolGeneratorParameter(name = parameter.name, value = parameter.default)
				elif isinstance(parameter, (NumericRangeGeneratorParameterSchema, NumericLabelGeneratorParameterSchema)):
					out = NumericGeneratorParameter(name = parameter.name, value = parameter.default)
				elif isinstance(parameter, (StringLiteralGeneratorParameterSchema, StringLabelGeneratorParameterSchema)):
					out = StringGeneratorParameter(name = parameter.name, value = parameter.default)
				if out:
					parameters.append(out)
			if do_debug:
				logger.info(f"{pprint.pformat(parameter)} --> {pprint.pformat(out)}")
		if do_debug:
			logger.info(f"Generated default parameters: {pprint.pformat(parameters)}")
		parameters = GeneratorParameters(action="generate", parameters = parameters)
		return parameters


	def _generate_worker(self, id:str, parameters:GeneratorParameters, do_stl=True, do_png=True, do_debug=False):
		if not id:
			return None, {"message":"No id provided while generating", "error": None}
		if not parameters:
			return None, {"message":"No parameters provided while generating {id}", "error": None}
		# We need the binary raw file so not using self.source()
		source = self.storage.download_file(id)
		if not source:
			return None, {"message":"Could not download source for {id}", "error": None}
		source_meta = self.storage.file_meta(id)
		if not source_meta:
			return None, {"message":"Could not download source for {id}", "error": None}
		logger.info(f"Source meta:{source_meta}")
		key = key = utils.calculate_unique_key(parameters.json())
		if not key:
			return None, {"message":"Could not generate derivative filenames for {id}", "error": None}
		source_name = source_meta.get("name", id)
		generator_type = GeneratorTypeEnum.openscad
		generator = generators_map.get(generator_type)
		if not generator:
			return None, f"Unknown or unsupported generator '{generator_type}' selected"
		return generator.generate(source_name = source_name, source = source, parameters = parameters, id = id, do_stl = do_stl, do_png = do_png, do_debug = do_debug)


	def generate(self, id:str, parameters:GeneratorParameters, do_stl = True, do_png = True, do_debug = False):
		stl_file_id = None
		png_file_id = None
		json_file_id = None
		log_file_id = None
		if do_stl:
			stl_file_id = self._find_derivative(id = id, parameters = parameters, mimetype = MIMETYPE_STL_MODEL)
		if do_png:
			png_file_id = self._find_derivative(id = id, parameters = parameters, mimetype = MIMETYPE_PNG_IMAGE)
		ret = None
		err = None
		if (do_stl and stl_file_id) or (do_png and png_file_id):
			# Model file found, gather the rest
			json_file_id = self._find_derivative(id = id, parameters = parameters, mimetype = MIMETYPE_JSON_DATA)
			log_file_id = self._find_derivative(id = id, parameters = parameters, mimetype = MIMETYPE_TEXT)
			ret = {
				  "model_id": stl_file_id
				, "parameters_id": json_file_id
				, "log_id": log_file_id
				, "thumbnail_id": png_file_id}
			err = None
			if do_debug:
				logger.info(f"Found existing derivative for '{id}'")
		else:
			# Model file did not exist, generate them
			logger.warning(f"No existing derivative found for '{id}', generating...")
			ret, err = self._generate_worker(id, parameters, do_stl=do_stl, do_png=do_png, do_debug=do_debug)
		if do_debug:
			logger.info(f"Returning {pprint.pformat(ret)} ({pprint.pformat(err)})")
		return ret, err


	def _generate_default_part_thumbnail_id(self, id, do_debug = True):
		if do_debug:
			logger.info(f"Generating default thumbnail for openscad file for {id}")
		source_schema, source_schema_err = self.source_schema(id = id, do_debug = do_debug)
		if not source_schema:
			logger.warning(f"Error fetching source_schema for id {id}: {pprint.pformat(source_schema_err)}")
			return None
		parameters = self._get_default_parameters(source_schema, do_debug = do_debug)
		# Perform a full generate while we are at it (it will take the same amount of time and will have to be done later anyways
		ret, err = self.generate(id = id, parameters = parameters, do_stl = True, do_png = True, do_debug = do_debug)
		if not ret or err:
			logger.warning(f"Error generating thumbnail: {pprint.pformat(err)}")
			return None
		thumbnail_id = ret.get("thumbnail_id")
		return thumbnail_id


	def _generate_default_part_thumbnail_url(self, id, do_debug = True):
		thumbnail_id = self._generate_default_part_thumbnail_id(id = id, do_debug = do_debug)
		if not thumbnail_id:
			logger.warning(f"No thumbnail found for id: {id}")
			return None, None
		data = self.get_derivative(id, thumbnail_id)
		if not data:
			logger.warning(f"Could not fetch data for thumbnail_id {pprint.pformat(thumbnail_id)}")
			return None, None
		if do_debug:
			logger.info(f"Setting default thumbnail for {id} to png of {len(data)} bytes")
		ret = self.set_drive_thumbnail_from_data(id, data, do_debug = do_debug)
		return ret, thumbnail_id


	def update_files(self, generate_thumbnails = False, do_debug = False):
		q = f"'{google_drive_folder_id}' in parents and name contains '.scad' and trashed=false"
		#self.files = files = self.storage.search_files(q, ["thumbnailLink"])

		files, folders = self.storage.recursive_search_worker(
			  folder_id = google_drive_folder_id
			#, f"trashed = false and name contains '.scad'"
			#, f"trashed = false and name not contains '.'"
			#, q_files = f"trashed = false and (name contains '.scad' or name contains '.ntop')" #TODO: Enable ntop support
			, q_files = f"trashed = false and (name contains '.scad')"
			, q_folders = f"trashed = false"
			, fields = ["thumbnailLink"]
			, path = list()
			, do_debug = do_debug) 
		
		self.files = files
		self.folders = folders
		
		#logger.info(pprint.pformat(self.files))
		#logger.info(f"PARTS:")
		self.parts_by_id = dict()
		self.parts = list()
		self.last_file_update = millinow()
		
		time_budget_millis = 60 * 1000 # a maximum of one minute of generation time is allowed per update
		update_start = millinow()
		for file in self.files:
			id = file.get("id")
			if id:
				mimetype = file.get("mimetype")
				format = understand_model_format(mimetype)
				if format:
					filename = file.get("name")
					path = file.get("path")
					tags = list()
					for p in path:
						tags.append(p.get("name"))
					basename = os.path.basename(filename)
					thumbnail_url = file.get("thumbnailLink")
					thumbnail_id = None
					if generate_thumbnails:
						logger.info(f"Doing thumbnail generation for {filename}")
						thumbnail_id = self._generate_default_part_thumbnail_id(id, do_debug = do_debug)
					else:
						source_schema, source_schema_err = self.source_schema(id = id, do_debug = do_debug)
						if source_schema:
							parameters = self._get_default_parameters(source_schema, do_debug = do_debug)
							if parameters:
								thumbnail_id = self._find_derivative(id = id, parameters = parameters, mimetype = MIMETYPE_PNG_IMAGE)
					part = {
						  "id":id
						, "title": basename
						, "mimetype": mimetype
						, "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
						, "filename": filename
						, "pretty_name": pretty_name(basename)
						, "tags": tags
						, "thumbnail_id": thumbnail_id
					}
					self.parts.extend([part])
					self.parts_by_id[id] = part
					#logger.info(f"Registering part: {pprint.pformat(part)}")
				else:
					logger.warning(f"Skipping file of unknown type: {mimetype}")
			else:
				logger.warning(f"Skipping part without id: {pprint.pformat(part)}")
					
	def maybe_update_files(self):
		since = millinow() - self.last_file_update
		if since > MIN_UPDATE_FREQ:
			self.update_files()
			return True
		return False

	def get_meta(self, id):
		self.maybe_update_files()
		return self.parts_by_id.get(id)

	def get_derivative(self, id, derivative_id):
		# TODO: For security, we should arrive at the ID fo the file to download indirectly
		data = self.storage.download_file(derivative_id)
		return data

	def get_parts(self):
		self.maybe_update_files()
		return self.parts
