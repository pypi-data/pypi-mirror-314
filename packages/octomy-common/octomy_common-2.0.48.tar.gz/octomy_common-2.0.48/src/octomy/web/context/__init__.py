from fastapi import Depends
from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import Any, Callable, Set, List, Optional, Annotated
import logging
import octomy.access
import octomy.config
import octomy.db
import pprint
import asyncio

logger = logging.getLogger(__name__)


try:
	from octomy.batch import Processor
	#raise ImportError
except ImportError:
	import sys
	import types

	# Check if 'octomy' module exists, if not create it
	if 'octomy' in sys.modules:
		octomy = sys.modules['octomy']
	else:
		octomy = types.ModuleType('octomy')
		sys.modules['octomy'] = octomy

	# Check if 'batch' submodule exists within 'octomy', if not create it
	if hasattr(octomy, 'batch'):
		batch = octomy.batch
	else:
		batch = types.ModuleType('batch')
		sys.modules['octomy.batch'] = batch
		octomy.batch = batch

	# Define the Processor class within octomy.batch
	class Processor:
		def __init__(self):
			print("octomy.batch.Processor is not installed. Using dummy Processor.")

		def is_dummy(self):
			return True
	logger.info("Asimilated batch processor")
	octomy.batch.Processor = Processor


DEFAULT_ADMIN_PATH="overwatch"

def url_for(name:str) -> str:
	url = f"http://CONTEXT_URL_FOR/{name}"
	logger.info(f"Generated url '{url}'")
	return  url



#required_scopes=["overwatch.access.profile.view"]
#required_scopes: List[str]

class Context(BaseSettings):
	config: octomy.config.OctomyConfig | None
	access: octomy.access.AccessContext | None
	db: octomy.db.Database | None
	bp: octomy.batch.Processor | None
#	current_user: Optional[octomy.access.User] = octomy.access.get_current_user()
#	url_for:Callable[[str], str] = url_for # SUBSTITUTE WITH NATIVE FASTAPI request.url_for() INSTEAD
	admin_path:str = DEFAULT_ADMIN_PATH
	required_scopes:List[str] = list()
	optional_attributes:dict = dict()
	#@property
	#def url_for(self, key) -> str:
	#	return url_for(key)
	webroot: str = "/app/webroot"
	password_cost_factor:int = 12
	def set_optional_attribute(self, name, value):
		self.optional_attributes[name] = value
	def __getattr__(self, name):
		if name in self.optional_attributes:
			val = self.optional_attributes.get(name)
			logger.info(f"Referencing optional attribute '{name}': {val}")
			return val
		logger.error(f"Trying to referene missing Context attribute '{name}'")
		return None


def default_decorator_function(undecorated_context:Context):
	return undecorated_context

_dec_fun = default_decorator_function

def set_context_decorator(dec_fun):
	_dec_fun = dec_fun



def scoped_context(s:list):
	return Annotated[Context, Depends(context_dependency(required_scopes=s))]


_context_singleton:Context = None

#@lru_cache
def get_context(required_scopes: Optional[List[str]] = None) -> Context:
	global _context_singleton
	do_debug = False
	if not _context_singleton:
		# We expect a list to be valid
		required_scopes = required_scopes or list()
		config:octomy.config.OctomyConfig = octomy.config.get_config()
		if None == config:
			config_error = "Unknown error"
			logger.error(f"Could not get config: {config_error}")
			return None
		db:octomy.db.Database | None = None
		bp:octomy.batch.Processor | None = None
		access:octomy.access.AccessContext | None = None
		result = octomy.db.get_database(config)
		db, db_err = result
		if not db:
			logger.warning(f"Could not get db: {db_err}")
		else:
			bp = octomy.batch.Processor(config = config, dbc = db)
			if not bp:
				bp_error = "Unknown error"
				logger.warning(f"Could not get config: {bp_error}")
			else:
				access = octomy.access.get_access_context(required_scopes)
				if not access:
					access_error = "Unknown error"
					logger.warning(f"Could not get config: {access_error}")
				else:
					if do_debug:
						logger.info(f"AccessContext: {pprint.pformat(access)}")
		context = Context(
			  config = config
			, access = access
			, db = db
			, bp = bp
			, admin_path = config.get("app-admin-path", DEFAULT_ADMIN_PATH)
			, required_scopes = required_scopes
		)
		_dec_fun(context)
		_context_singleton = context
	return _context_singleton


# Helper dependency
def context_dependency(required_scopes: Optional[List[str]] = None):
	async def dependency():
		return get_context(required_scopes = required_scopes or list())
	return dependency




###########################################

'''
TODO: Fix access

from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase

class ContextScheme(SecurityBase):

	def __init__(
		  self
		, scopes: Annotated[
			Optional[List[str]],
			Doc(
				"""
				The seucirty scopes required by the endpoint that depends on this schema instance
				"""
			),
		] = None
		, needsAuth: Annotated[
		bool,
		Doc(
			"""
			Whether or not we need a user that is authenticated
			"""
		),
		] = True
		, tokenUrl: Annotated[
			str,
			Doc(
				"""
				The URL to obtain the OAuth2 token. This would be the *path operation*
				that has `OAuth2PasswordRequestForm` as a dependency.
				"""
			),
		] = "token"

	):
		# Magic to make fastapi openapi happy
		self.model: APIKey = APIKey(
			**{"in": APIKeyIn.query},  # type: ignore[arg-type]
			name = "octomy_auth_cookie",
			description = "octomy_auth_cookie",
		)
		self.scheme_name = self.__class__.__name__
		self.tokenUrl = tokenUrl
		self.scopes = scopes or list()
		logger.info(f"ContextScheme.init(scopes={pprint.pformat(self.scopes)}, tokenUrl={pprint.pformat(self.tokenUrl)})");

	async def __call__(self, request:Request, cookie: str = Depends (api_cookie)) -> Context:
		do_debug = True
		local_user, local_user_err = get_current_local_user(cookie)
		user = None
		if local_user:
			user = User()
			user.local_user = local_user
		else:
			logger.error(f"Could not get user: {local_user_err}")
			
		return await get_context(user)
		
# Convenience export
Depends = fastapi.Depends
'''


