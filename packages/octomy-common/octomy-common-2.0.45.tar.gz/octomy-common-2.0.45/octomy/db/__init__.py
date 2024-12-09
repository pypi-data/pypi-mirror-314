#!/bin/env python3
from functools import lru_cache
from furl import furl
from typing import Type, get_args, get_origin
import aiofiles
import asyncio
import datetime
import fastapi.encoders
import logging
import octomy.utils
import os
import pathlib
import pprint
import psycopg
import psycopg_pool
import pydantic
import re
import socket
import urllib.parse


logger = logging.getLogger(__name__)


c = octomy.utils.termcol

def pydantic_to_params(params):
	if isinstance(params, pydantic.BaseModel):
		return fastapi.encoders.jsonable_encoder(params)
	elif isinstance(params, dict):
		return {k: fastapi.encoders.jsonable_encoder(v) for k, v in params.items()}
	else:
		return params


def schema_to_compact(schema: dict) -> str:
	# Extract the title or name of the model
	model_name = schema.get('title', 'UnknownModel')
	
	# Initialize an empty list to hold field descriptions
	field_descriptions = []
	
	# Iterate over the properties in the schema to build field descriptions
	for field_name, details in schema.get('properties', {}).items():
		field_type = details.get('type', 'UnknownType')
		
		# For more complex types (e.g., arrays, nested models), you might need additional handling here
		if field_type == 'array':
			items = details.get('items')
			if isinstance(items, dict):
				item_type = items.get('type', 'UnknownType')
				field_type = f"List[{item_type}]"
		
		# Append the field description to the list
		field_descriptions.append(f"{field_name}:{field_type}")
	
	# Join all field descriptions into a single string
	fields_str = ', '.join(field_descriptions)
	
	# Return the compact representation of the model
	return f"{model_name}{{ {fields_str} }}"


def describe_type(input_type: Type) -> str:
	# Handle Pydantic models by checking for the .schema() method
	if hasattr(input_type, 'schema') and callable(getattr(input_type, 'schema')):
		schema = schema_to_compact(input_type.schema())
		return f"Pydantic {schema}"
	
	# Check for generic types (e.g., List[SomeType])
	origin_type = get_origin(input_type)
	if origin_type is not None:
		type_args = get_args(input_type)
		type_args_descriptions = [describe_type(t) for t in type_args]
		descs='\n, '.join(type_args_descriptions)
		return f"Generic type: {origin_type.__name__} of [{descs}]"
	# Fallback for standard or simple types
	return f"Type: {input_type}"


def diag_to_str(diag, prefix =""):
	error_attrs = [
		"column_name", "constraint_name", "context", "datatype_name",
		"internal_position", "internal_query", "message_detail", "message_hint",
		"message_primary", "schema_name", "severity", "source_file",
		"source_function", "source_line", "sqlstate", "statement_position",
		"table_name", "severity_nonlocalized"
	]
	out = ""
	for attr in error_attrs:
		value = getattr(diag, attr, None)  # Use getattr to safely handle missing attributes
		if value is not None:  # Only log if the attribute is present and not None
			out += f"{prefix}{attr}: {value}"
	return out

def _q(s):
	if not s:
		return ""
	return urllib.parse.quote(s)

def check_host(hostname, port, timeout_sec = 4):
	try:
		ip_address = socket.gethostbyname(hostname)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(timeout_sec)
		result = sock.connect_ex((ip_address, port))
		sock.close()
		if result == 0:
			return True, None
		else:
			return False, f"Port '{port}' is not open on '{hostname}'"
	except socket.gaierror:
		return False, f"Hostname '{hostname}' could not be resolved"
	except socket.timeout:
		return False, f"Connection to the host timed out after {timeout_sec}"
	except Exception as e:
		return False, f"An unexpected error has occurred: {e}"


def verify_db_uri(db_uri, do_online = True):
	def _error(err):
		return None, err
	try:
		result:ParseResult = urllib.parse.urlparse(db_uri)
		#logger.warning(f"{result}")
		if not result:
			return _error(f"DB URI '{db_uri}' could not be pased")
		if result.scheme != 'postgresql' and result.scheme != 'postgres':
			return _error(f"DB URI '{db_uri}' did not have correct schema: '{result.scheme}'")
		if not result.hostname:
			return _error(f"DB URI '{db_uri}' did not have hostname")
		if not result.username:
			return _error(f"DB URI '{db_uri}' did not have username")
		if not result.password:
			return _error(f"DB URI '{db_uri}' did not have password")
		if not result.path.strip('/'):
			return _error(f"DB URI '{db_uri}' did not have database path")
		if do_online:
			try:
				host_ok, host_err = check_host(result.hostname, result.port)
				if not host_ok:
					return None, host_err
				#logger.warning("ONLINE IS GOPING DOWN")
				with psycopg.connect(db_uri) as connection:
					#logger.warning("ONLINE IS GOOD")
					pass
			except psycopg.Error as e:
				diag = diag_to_str(e.diag, prefix = ", ")
				return _error(f"Could not connect with DB URI '{db_uri}': {e} ({type(e)}), diag={diag}, sqlstate={e.sqlstate}, pgconn={e.pgconn}")
	except Exception as e:
		return _error(f"DB URI '{db_uri}' had error while parsing: {e} ({type(e)})")
	return db_uri, None


def db_uri_from_conf(config, do_verify = True, do_online= True, do_redact = False):
	if None == config:
		return None, "No config"
	db_hostname = config.get("db-hostname", None)
	db_port = config.get("db-port", None)
	db_username = config.get("db-username", None)
	db_password = config.get("db-password", None)
	db_database = config.get("db-database", None)
	if do_redact:
		db_password = octomy.utils.redact(db_password)
	f = furl()
	try:
		f.set(scheme="postgres", username = db_username, password = db_password, host = db_hostname, port = db_port, path = db_database)
		if do_verify:
			 return verify_db_uri(f.url, do_online = do_online)
		else:
			return f.url, None
	except Exception as e:
		#logger.error(e, exc_info=e)
		return None, f"Invalid parts: {e} {type(e)}"


def db_uri_to_config(db_uri, do_online = True):
	db_uri_out, err = verify_db_uri(db_uri, do_online = do_online)
	if not db_uri_out:
		#logger.warning(err)
		return {}
	f = furl(db_uri)
	database = (f.path.segments or [""])[0]
	# fmt:off
	config = {
		  "db-hostname": f.host
		, "db-port": f.port
		, "db-username": f.username
		, "db-password": f.password
		, "db-database": database
	}
	# fmt:on
	return config


def get_config_hash(config, prefix = "db-"):
	if not config:
		return ""
	key = ""
	for i in ["hostname", "port", "username", "password", "database"]:
		key += octomy.utils.hashstr(config.get(f"{prefix}{i}", ""))
	return octomy.utils.hashstr(key)


def query_key_to_sql_path(query_key, relative=False, do_debug = True):
	sep = '.'
	if do_debug:
		logger.info(f"                   sep:{sep}")
		logger.info(f"             query_key:{query_key}")
	parts = query_key.split(sep) if sep in query_key else list()
	if do_debug:
		logger.info(f"                 parts: '{pprint.pformat(parts)}'")
	if not parts:
		logger.warning(f"query_key '{query_key}' could not be split")
		return None
	if len(parts) <= 0:
		logger.warning(f"query_key '{query_key}' split into 0")
		return None
	script_name = parts.pop() + ".sql"
	relative_script_path = os.path.join(*parts, "sql", script_name)
	if relative:
		if do_debug:
			logger.info(f"Parsed '{query_key}' to '{relative_script_path}' (relative)")
		return relative_script_path
	package_name = sep.join(parts)
	if do_debug:
		logger.info(f"          package_name:{package_name}")
	package_dir = octomy.utils.get_package_root_dir(package_name, do_debug = do_debug)
	if do_debug:
		logger.info(f"  get_package_root_dir:{package_dir}")
	if not package_dir:
		logger.warning(f"get_package_root_dir failed for '{package_name}'")
		return None
	package_dir = package_dir.parent
	canonical_path = os.path.join(package_dir, relative_script_path)
	canonical_path = pathlib.Path(canonical_path).resolve()
	if do_debug:
		logger.info(f"        canonical_path:{canonical_path}")
	return canonical_path


################################################################################



class DbTime(pydantic.BaseModel):
	now:datetime.datetime


################################################################################


class Database:
	def __init__(self, db_uri):
		self.error = None
		self.db_uri = db_uri
		#self.query_dirs = set()
		self.queries = dict()
		self.pool = None

	def _error(self, message):
		ok = not bool(message)
		# logger.info(f"_error({message}) -> {ok}")
		self.error = None if ok else message
		return ok, self.error

	# Get current time from db
	#def get_now(self, do_debug=False) -> DbTime, str|None:
	#	db_ret, db_err = await self.dbc.query_one("octomy.db.get_now", params=dict(), item_type=DbTime, prepare=False, do_debug=do_debug)
	#	return db_ret, db_err

	async def verify(self, do_online = False):
		try:
			# logger.info(f"VERIFYING '{self.db_uri}'")
			if not self.db_uri:
				return self._error(f"No DB URI: '{self.db_uri}'")
			out, err = verify_db_uri(self.db_uri, do_online = do_online)
			if not out:
				return self._error(err)
			#if not self.query_dirs or len(self.query_dirs) <= 0:
			#	return self._error(f"No query dirs registered: '{self.query_dirs}'")
			return True, None
		except Exception as e:
			logger.warning(f"Unknown error '{e}':", exc_info=True)
			return False, str(e)

	async def state(self, do_online = False, show_full = False):
		head_c=c.GREEN
		logger.info(f"{head_c}Status [{c.ORANGE}{'ONLINE' if do_online else 'OFFLINE'}{head_c}]:")
		ok, err = await self.verify(do_online = do_online)
		if ok:
			logger.info(f"\t{c.GREEN}OK")
		else:
			logger.info(f"\t{c.RED}ERROR: {c.ORANGE}{err}")
		#if self.query_dirs:
		#	logger.info(f"{head_c}Query paths:")
		#	for query_dir in self.query_dirs:
		#		logger.info(f"\t{c.CYAN}{query_dir}")
		#else:
		#	logger.info("No query paths")
		if self.queries:
			logger.info(f"{head_c}Loaded queries:")
			tabs2 = "\t\t"
			for key, query in self.queries.items():
				if show_full:
					logger.info(f"\t{c.BLUE}{key:>10}{c.ENDC}: {c.GREEN}{octomy.utils.indent(query, tabs2)}")
				else:
					logger.info(f"\t{c.BLUE}{key:>10}{c.ENDC}: {c.GREEN}{len(query)} chars")
		else:
			logger.info(f"{head_c}No loaded queries")
		return ok, err

	def reset_queries(self):
		"""Reset the internal cache of queries, forcing queries to be reloaded upon next invocation"""
		self.queries = dict()
		'''
	def preload_queries(self, do_debug = False):
		"""Recursively load and register queries from .sql files in given path."""
		self.reset_queries()
		if do_debug:
			logger.info("Scanning query dirs:")
		for dir in self.query_dirs:
			if not os.path.isdir(dir):
				if do_debug:
					logger.warning(f"Not a dir, skipping: '{dir}'")
					logger.warning(f" * NOTE: CWD is '{os.getcwd()}'")
				continue
			if do_debug:
				logger.info(f" *Scanning query dir: '{dir}'")
			for sql_file in dir.rglob('*.sql'):
				# some/path/file.sql --> some.path.file
				if do_debug:
					logger.info(f" |-Found candidate file: '{sql_file}'")
				query_key = sql_file.relative_to(dir).with_suffix('').as_posix().replace('/', '.')
				with open(sql_file, 'r', encoding='utf-8') as file:
					query = file.read()
					if do_debug:
						#logger.info(f" | |-Loading '{query_key}' from '{sql_file}' with '{query}'")
						logger.info(f" | |-Loading '{query_key}' from '{sql_file}' with query size {len(query)} chars")
					self.queries[query_key] = query

		if do_debug:
			logger.info("Scanning complete")


	def register_query_dir(self, path, do_preload = False, do_debug = False):
		"""Recursively load queries from .sql files in given path."""
		real = os.path.realpath(path)
		if do_debug:
			logger.info(f"Adding query dir: '{path}' ({real})")
		self.query_dirs.add(pathlib.Path(real))
		if do_preload:
			self.preload_queries(do_debug = do_debug)
'''

	async def load_query(self, query_key, do_debug = False):
		"""Load and return a single query by first looking it up in the internal cache and falling back on looking for it on disk"""
		# Cache hit
		if query_key in self.queries:
			return self.queries[query_key]
		file_path = None
		# Cache miss, load from disk
		try:
			# Make sure we know where to look
			#if len(self.query_dirs) <= 0:
			#	raise Exception(f"No query dir(s) specified")
			file_path = query_key_to_sql_path(query_key, relative=False, do_debug = do_debug)
			if do_debug:
				logger.info(f"             file_path: '{file_path}'")
			if not file_path:
				raise Exception(f"No path found for {query_key}")
			# Read the SQL query from file
			async with aiofiles.open(file_path, mode='r', encoding='utf-8') as file:
				sql_query = await file.read()
				self.queries[query_key] = sql_query
				return sql_query
			'''
			# Convert the query_key to a file path
			for dir in self.query_dirs:
				file_path = dir / pathlib.Path(query_key.replace('.', '/') + '.sql')
				logger.info(f"file_path {file_path}")
					
				# Read the SQL query from file
				async with aiofiles.open(file_path, mode='r', encoding='utf-8') as file:
					sql_query = await file.read()
				# with open(file_path, 'r', encoding='utf-8') as file:
				#	sql_query = file.read()
				self.queries[query_key] = sql_query
				return sql_query
			'''
		except FileNotFoundError:
			logger.info(f"SQL file {os.path.abspath(file_path)}")
			logger.error(f"SQL file not found for key {query_key} at path {file_path}")
		except Exception as e:
			logger.info(f"SQL file '{file_path}'")
			logger.error(f"{type(e).__name__}: Error loading SQL file for key {query_key}: {e}")
			logger.exception(e)
		return None

	def _get_pool(self):
		self.pool = self.pool or psycopg_pool.AsyncConnectionPool(self.db_uri)
		return self.pool

	def _adapt(self, raw, item_type, do_debug=False):
		if not item_type:
			return raw
		if do_debug:
			logger.info(f"Adapting {pprint.pformat(raw)} to {pprint.pformat(item_type)}")
		try:
			return pydantic.TypeAdapter(item_type).validate_python(raw)
		except Exception as e:
			logger.warning(f"Adaption error details")
			logger.warning(f"                       raw: {pprint.pformat(raw)}")
			logger.warning(f"                 type(raw): {type(raw)}")
			logger.warning(f"                 item_type: {item_type}")
			logger.warning(f"  describe_type(item_type): {describe_type(item_type)}")
			raise

	async def direct_query(self, query, query_name=None, params=dict(), mode="none", item_type=None, prepare=True, do_debug=True):
		cursor = None
		try:

			params = pydantic_to_params(params)
			
			if not query:
				raise Exception("No query")
			# Make sure we actually have a pool
			pool = self._get_pool()
			if not pool:
				raise Exception("No pool")
			# TODO: Look into implementing pipeline mode
			# See: https://www.psycopg.org/psycopg3/docs/advanced/pipeline.html
			# Acquire a connection from the pool
			async with pool.connection() as connection:
				async with connection.transaction() as transaction:
					async with connection.cursor(row_factory=psycopg.rows.dict_row) as cursor:
						# See https://www.psycopg.org/psycopg3/docs/advanced/prepare.html
						if do_debug:
							logger.info(f"Preparing query '{query_name}'")
							logger.info("\n\n" + query+"\n\n")
							logger.info(f"With data")
							logger.info("\n\n" + pprint.pformat(params)+"\n\n")
						await cursor.execute(query = query, params = params, prepare = prepare)
						if mode == "many":
							res = self._adapt(await cursor.fetchall(), item_type, do_debug)
							if do_debug:
								logger.info(f"Returning many data: '{pprint.pformat(res)}'")
							return res, None
						elif mode == "one":
							res = self._adapt(await cursor.fetchone(), item_type, do_debug)
							if do_debug:
								logger.info(f"Returning one data: '{pprint.pformat(res)}'")
							return res, None
						elif mode == "exists":
							res = await cursor.fetchone()
							if item_type:
								logger.warning(f"item_type speficied '{item_type}' for query with mode exists")
							if do_debug:
								logger.info(f"Returning exist data: '{pprint.pformat(res)}'")
							return res is not None, None
						elif mode == "none":
							if item_type:
								logger.warning(f"item_type speficied '{item_type}' for query with mode none")
							if do_debug:
								logger.info(f"Returning for none")
							return None, None
						else:
							raise Exception(f"Unknown mode {mode}. Should be one of [many, one, exists, none]")
		except Exception as e:
			logger.error("\n\n"+octomy.utils.stripes())
			logger.error("")
			logger.error("")
			logger.error(f"###############################################")
			logger.error(f"+       Error: ({type(e).__name__})")
			logger.error(f"#    Querying: '{query_name}'\n\n{query}\n")
			if cursor and query and "cursor" in query:
				logger.error(f"#    Injected: '{cursor.query.decode()}'")
			logger.error(f"#         On")
			logger.error(f"#         + db_uri =   '{self.db_uri}'")
			logger.error(f"#         For")
			logger.error(f"#         + mode =   '{mode}'")
			logger.error(f"#         + params = '{pprint.pformat(params)}'")
			logger.error(f"# Failed with:")
			if isinstance(e,psycopg.Error):
				logger.error(f"# + e.type:     '{type(e).__name__}'")
				logger.error(f"# + e.sqlstate: '{e.sqlstate}'")
				if getattr(e, "pgconn", None):
					logger.error(f"# + e.pgconn:   '{e.pgconn}'")
				if getattr(e, "pgresult", None):
					logger.error(f"# + e.pgresult: '{e.pgresult}'")
				if e.diag:
					logger.error(f"# + e.diag: '{e.diag}'")
					logger.error(diag_to_str(e.diag, prefix = "#   + "))
			elif isinstance(e, pydantic.ValidationError):
				logger.error(f"Validation error: with item_type '{item_type}'")
			else:
				# Unexpected errors
				logger.error(f"Unexpected error: {type(e).__name__}")
			logger.error(f"#  Stacktrace: \n\n{e}\n")
			logger.error("\n\n"+octomy.utils.stripes())
			return None, str(e)

	async def key_query(self, query_key, params=dict(), mode="none", item_type=None, prepare=True, do_debug=False):
		query = await self.load_query(query_key, do_debug = do_debug)
		if query:
			if do_debug:
				logger.info(f"key_query params='{pprint.pformat(params)}' prepare={prepare}")
			return await self.direct_query(query = query, query_name=query_key, params = params, mode = mode, item_type=item_type, prepare=prepare, do_debug=do_debug)
		return None, "No query"

	async def query_many(self, query_key, params=dict(), item_type=None, prepare=True, do_debug=False):
		if do_debug:
			logger.info(f"query_many params='{pprint.pformat(params)}' prepare={prepare}")
		return await self.key_query(query_key = query_key, params = params, mode = "many", item_type=item_type, prepare=prepare, do_debug=do_debug)

	async def query_one(self, query_key, params=dict(), item_type=None, prepare=True, do_debug=False):
		if do_debug:
			logger.info(f"query_one params='{pprint.pformat(params)}' prepare={prepare}")
		return await self.key_query(query_key = query_key, params = params, mode = "one", item_type=item_type, prepare=prepare, do_debug=do_debug)

	async def query_none(self, query_key, params=dict(), prepare=True, do_debug=False):
		if do_debug:
			logger.info(f"query_none params='{pprint.pformat(params)}' prepare={prepare}")
		return await self.key_query(query_key = query_key, params = params, mode = "none", prepare=prepare, do_debug=do_debug)

	async def query_exists(self, query_key, params=dict(), prepare=True, do_debug=False):
		if do_debug:
			logger.info(f"query_exists params='{pprint.pformat(params)}' prepare={prepare}")
		return await self.key_query(query_key = query_key, params = params, mode = "exists", prepare=prepare, do_debug=do_debug)


#@lru_cache
def get_database(config:dict, do_verify=True, do_online = True, do_debug = True):
	uri, err = db_uri_from_conf(config = config, do_verify = do_verify, do_online = do_online, do_redact = False)
	if not uri:
		logger.warning(f"db uri error: {err}")
		return None, err
	db = Database(db_uri = uri)
	if False:
		sql_dir = config.get("db-sql-dir")
		if sql_dir:
			if do_debug:
				logger.info(f"Adding sql dir from config: {sql_dir}")
			db.register_query_dir(sql_dir, do_debug = do_debug)
	return db, None

