#!/bin/env python3
import aiofiles
import asyncio
import logging
import os
import pathlib
import pprint
import psycopg
import psycopg_pool
import re


logger = logging.getLogger(__name__)


def stripes(cols=79, rows=3, on=3, off=3, on_char="#", off_char=" ", offset=0, sheer=1):
	out=""
	alphabet = on_char * on + off_char * off
	alphabet_len=len(alphabet)
	for row in range(0, rows):
		index = offset
		for col in range(0, cols):
			alphabet_index = index % alphabet_len
			out += alphabet[alphabet_index]
			index += 1
		offset+=sheer
		out+="\n"
	return out

def log_exception(e):
	if isinstance(e, asyncpg.PostgresError):
		# Log detailed database error information
		logger.error(f"+ Postgres error ({type(e).__name__}): e={e}")
		logger.error(f"+ Detail: {e.detail}")
		logger.error(f"+ Hint: {e.hint}")
	else:
		# Log non-database errors
		logger.error(f"+ NON DB ERROR ({type(e).__name__}): e={e}")

	# Log traceback
	logger.error("Traceback (most recent call last):")
	traceback.print_exception(type(e), e, e.__traceback__)
	
def log_db_exception(e, query_key, params):
	logger.error("\n" * 2)
	logger.error("#" * 50)
	logger.error(f"Querying: {query_key}")
	logger.error(f"Using data: {pprint.pformat(params)}")
	logger.error(f"Failed with:")
	log_exception(e)
	logger.error("#" * 45)
	logger.error("\n" * 2)

class Database:
	def __init__(self, db_uri):
		self.db_uri = db_uri
		self.query_dir = None
		self.queries = dict()
		self.prepared = dict()
		self.pool = None


	async def prepare_query(self):
		 statement = await conn.prepare("SELECT * FROM my_table WHERE id = $1")
		 
	async def preload_queries(self, path):
		"""Recursively load and register queries from .sql files in given path."""
		self.query_dir = pathlib.Path(path)
		for sql_file in self.query_dir.rglob('*.sql'):
			# some/path/file.sql --> some.path.file
			query_key = sql_file.relative_to(self.query_dir).with_suffix('').as_posix().replace('/', '.')
			with open(sql_file, 'r', encoding='utf-8') as file:
				self.queries[query_key] = file.read()

	def reset_queries(self):
		"""Reset the internal cache of queries, forcing queries to be reloaded upon next invocation"""
		self.queries=dict()
		self.prepared=dict()

	async def load_query(self, query_key):
		"""Load and return a single query by first looking it up in the internal cache and falling back on looking for it on disk"""
		# Cache hit
		if query_key in self.queries:
			return self.queries[query_key]
		# Cache miss, load from disk
		try:
			# Convert the query_key to a file path
			file_path = self.query_dir / pathlib.Path(query_key.replace('.', '/') + '.sql')
			logger.info(f"file_path {file_path}")
				
			# Read the SQL query from file
			async with aiofiles.open(file_path, mode='r', encoding='utf-8') as file:
				sql_query = await file.read()
			# with open(file_path, 'r', encoding='utf-8') as file:
			#	sql_query = file.read()
			self.queries[query_key] = sql_query
			return sql_query
		except FileNotFoundError:
			logger.info(f"SQL file {os.path.abspath(file_path)}")
			logger.error(f"SQL file not found for key {query_key} at path {file_path}")
		except Exception as e:
			logger.error(f"Error loading SQL file for key {query_key}: {e}")

	def _get_pool(self):
		self.pool = self.pool or psycopg_pool.AsyncConnectionPool(self.db_uri) # , min_size=min_conn, max_size=max_conn
		return self.pool

	async def direct_query(self, query, params=dict(), mode="none"):
		try:
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
						logger.info(f"Preparing query with data: '{pprint.pformat(params)}'")
						await cursor.execute(query = query, params = params, prepare = True)
						if mode == "many":
							res = await cursor.fetchall()
							return res, None
						elif mode == "one":
							return await cursor.fetchone(), None
						elif mode == "exists":
							res = await cursor.fetchone(), None
							return res is not None
						elif mode == "none":
							return None, None
						else:
							raise Exception(f"Unknown mode {mode}. Should be one of [many, one, exists, none]")
		except Exception as e:
			logger.error("\n\n"+stripes())
			logger.error("")
			logger.error("")
			logger.error(f"###############################################")
			logger.error(f"#    Querying: \n\n{query}\n")
			if cursor and query and "cursor" in query:
				logger.error(f"#    Injected: '{cursor.query.decode()}'")
			logger.error(f"#         For")
			logger.error(f"#         + mode =   '{mode}'")
			logger.error(f"#         + params = '{pprint.pformat(params)}'")
			logger.error(f"# Failed with:")
			if isinstance(e,psycopg.Error):
				logger.error(f"# + e.type:     '{type(e).__name__}'")
				logger.error(f"# + e.detail:   '{e}'")
				logger.error(f"# + e.sqlstate: '{e.sqlstate}'")
				if getattr(e, "pgconn", None):
					logger.error(f"# + e.pgconn:   '{e.pgconn}'")
				if getattr(e, "pgresult", None):
					logger.error(f"# + e.pgresult: '{e.pgresult}'")
				if e.diag:
					logger.error(f"# + e.diag: '{e.diag}'")
					error_attrs = [
						"column_name", "constraint_name", "context", "datatype_name",
						"internal_position", "internal_query", "message_detail", "message_hint",
						"message_primary", "schema_name", "severity", "source_file",
						"source_function", "source_line", "sqlstate", "statement_position",
						"table_name", "severity_nonlocalized"
					]
					for attr in error_attrs:
						value = getattr(e.diag, attr, None)  # Use getattr to safely handle missing attributes
						if value is not None:  # Only log if the attribute is present and not None
							logger.error(f"#   + {attr}: {value}")
			else:
				# Unexpected errors
				logger.info(f"Unexpected error: {type(e).__name__}: {e}")
				
			logger.error("\n\n"+stripes())
			return None, str(e)


	async def _key_query_worker(self, query_key, params=dict(), mode="none"):
		query = await self.load_query(query_key)
		logger.info("_key_query_worker params='{pprint.pformat(params)}'")
		return await self.direct_query(query = query, params = params, mode = mode)

	async def query_many(self, query_key, params):
		logger.info("query_many params='{pprint.pformat(params)}'")
		return await self._key_query_worker(query_key = query_key, params = params, mode = "many")

	async def query_one(self, query_key, params):
		logger.info("query_one params='{pprint.pformat(params)}'")
		return await self._key_query_worker(query_key = query_key, params = params, mode = "one")

	async def query_none(self, query_key, params):
		logger.info("query_none params='{pprint.pformat(params)}'")
		return await self._key_query_worker(query_key = query_key, params = params, mode = "none")

	async def query_exists(self, query_key, params):
		logger.info("query_exists params='{pprint.pformat(params)}'")
		return await self._key_query_worker(query_key = query_key, params = params, mode = "exists")


	async def execute_old(self, query_key, **params):
		"""Execute a registered query by its key."""
		if query_key not in self.queries:
			raise ValueError(f"Query '{query_key}' not found.")
		
		async with self.pool.connection() as connection:
			async with connection.cursor() as cur:
				await cur.execute(self.queries[query_key], params)
				# Assuming a fetch is needed, adjust as necessary
				return await cur.fetchall()
