import os
import pprint

from pathlib import Path
import json
import base64

import ast
import octomy.utils
import logging
from functools import lru_cache

from markupsafe import Markup

import yaml

try:
	from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
	from yaml import Loader, Dumper



logger = logging.getLogger(__name__)


class c:
	HEADER = '\033[95m'
	BLUE = '\033[94m'
	CYAN = '\033[96m'
	GREEN = '\033[92m'
	RED = '\u001b[31m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'



# IMPORTANT!!!!!!
# DO NOT PUT REAL CONFIG HERE, ESPECIALLY PASSWORDS AND OTHER SENSITIVE DATA!!!!
unset = "OVERRIDE ME, THIS IS A DEFAULT"

'''

defaults = {
	  "DEBUG": False
	, "TESTING": False
	, "SECRET_KEY": base64.b64encode(os.urandom(16)).decode("utf-8")
	, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
	, "SQLALCHEMY_ECHO": False
	, "SQLALCHEMY_TRACK_MODIFICATIONS": True
	, "batch-filter-root": "/app/fk/batch/filters"
	, "cache-dir-name": "_cache"
	, "crawler-html-parser": "html5lib"
	, "crawler-referer": "https://www.shopify.com/"
	, "crawler-socket-timeout": 15
	, "crawler-user-agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
	, "db-database": "postgres"
	, "db-hostname": "localhost"
	, "db-password": unset
	, "db-port": "5432"
	, "db-username": unset
	, "db-sql-dir": "sql"
	, "smtp-hostname": unset
	, "smtp-port": "2525"
	, "smtp-user": unset
	, "smtp-password": unset
	, "smtp-headers": unset
	, "influx-dbname": "sales"
	, "influx-hostname": "localhost"
	, "influx-password": unset
	, "influx-port": "8086"
	, "influx-username": unset
	, "n2report-dir-name": "_n2report"
	, "n2report-index-name": "index.html"
	, "overwatch-password": unset
	, "overwatch-user": unset
	, "preferred-url-scheme": "http"
	, "printful-api-endpoint": "https://api.printful.com/"
	, "printful-api-key": unset
	, "printful-api-key-base64": unset
	, "screenshots-dir-name": "_screenshots"
	, "screenshots-index-name": "screenshots.html"
	, "shop-id-generator-batch-size": 200
	, "shop-id-generator-max": 25000000000  # billions
	, "shop-id-generator-min": 0
	, "shop-id-thread-count": 300
	, "shopify-api-key": unset
	, "shopify-api-secret": unset
	, "shopify-api-throttle-limit": 1
	, "shopify-api-throttle-period": 3000
	, "shopify-api-version": "2020-10"
	, "shopify-app-domain": unset
	, "shopify-app-author": "The author of this app"
	, "shopify-app-author-email": "The email of the author of this app"
	, "shopify-app-company-name": "The name of the company behind this app"
	, "shopify-app-company-website": "The url fo the company website"
	, "shopify-app-description": "The description of this app"
	, "shopify-app-name": "The name of this app"
	, "shopify-app-preferred-url-scheme": "https"
	, "shopify-password": unset
	, "shopify-shared-secret": unset
	, "static-files-root": "/app/shopify_app/static"
	, "webdriver-max-windows": 5
	, "webdriver-url": "http://127.0.0.1:4444/wd/hub"
	, "webdriver-wait-time-sec": 10
	
	
	, "app-name": Markup("Korall&trade;")
	, "app-url": Markup("https://korall.io")
	, "app-contact-email": Markup("contact@korall.io")
	, "app-contact-telephone": Markup("+47 942 37 478")
	, "app-webmaster-email": Markup("webmaster@korall.io")
	, "app-linkedin": Markup("korall-engineering-as")
	, "app-instagram": Markup("korall_engineering")
	, "app-logo": "/static/images/Korall_Engineering_logo.svg"
	, "app-logo-dark": "/static/images/Korall_Engineering_logo_dark.svg"
	, "app-slogan": Markup("Challenge creation&trade;")
	, "app-geo-lat": 60.37776008039476
	, "app-geo-lon": 5.331693878840272
	, "app-geo-zoom": 19
	, "app-description": Markup("Korall Engineering AS is a design engineering firm, part of StartupLab Bergen, that employs the latest high-end product optimization technologies")
	, "app-admin-path": "overwatch"

	, "app-unknown-user-image": "/static/images/unknown-user.svg"
	, "app-db-fetch-limit": 1000
	
	# "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36"
	# SHOPIFY_SHOP_NAME = 'firstkissdesigns'
	# https://flask.palletsprojects.com/en/1.1.x/config/#DEBUG
	# https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY
	# SERVER_NAME = "localhost.localdomain:5000"
	# https://flask.palletsprojects.com/en/1.1.x/config/#TESTING
}

'''


class OctomyConfig(dict):
	def __init__(self):
		super().__init__()
		self.sources = dict()


	def TO_BOOL(str):
		"""Helper to parse boolean from environment variable"""
		if str.lower() in {"1", "t", "true"}:
			return True
		elif str.lower() in {"0", "f", "false"}:
			return False
		return None

	# With help from https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except
	def TO_UINT(str):
		"""Helper to parse unsigned integer from environment variable"""
		if str.isdigit():
			return int(str)
		if str.startswith("+") and str[1:].isdigit():
			return int(str)
		return None


	def TO_INT(str):
		"""Helper to parse signed integer from environment variable"""
		if str.isdigit():
			return int(str)
		if str.startswith(("+", "-")) and str[1:].isdigit():
			return int(str)
		return None


	def TO_ENV_KEY(str):
		"""Helper to convert a string to environment variable name on the form THIS_IS_ENV_VARIABLE"""
		str = str.strip().upper()
		for i in ["-", " ", "\t"]:
			str = str.replace(i, "_")
		return str


	def TO_GUESS_TYPE(str):
		"""Helper to convert a string to a native python type"""
		b = OctomyConfig.TO_BOOL(str)
		if b is not None:
			return b
		ret = str
		try:
			ret = ast.literal_eval(str)
		except:
			pass
		return ret


	def apply_environment_variables(self, do_debug=False):
		"""Helper to load configuration values from environment variables"""
		if do_debug:
			logger.info(f"apply_environment_variables()")
		ct = 0
		for key, value in self.items():
			# Try with bare key first
			env_value = os.environ.get(key, default=None)
			if do_debug:
				logger.info(f" {key}: {env_value}")
			if not env_value:
				# Try with "envified" key second
				env_key = OctomyConfig.TO_ENV_KEY(key)
				env_value = os.environ.get(env_key, default=None)
				if do_debug:
					logger.info(f" {env_key}: {env_value}")
			if env_value:
				old_value = self.get(key)
				old_source = self.sources.get(key)
				if old_value:
					if do_debug:
						logger.info(f"Overwriting existing value {old_value} from {old_source}")
				self[key] = OctomyConfig.TO_GUESS_TYPE(env_value)
				self.sources[key] = "environment"
				ct += 1
				# logger.info(f"Value from env '{env_value}' replaced '{value}' for key '{key}'")
			else:
				# logger.warning(f"WARNING: No {env_key} in env, using last value '{key}' = {value}")
				pass
		logger.info(f"Put {ct} values from environment variables into configuration")
		return True

	def apply_dict(self, new_values, source="dict", do_debug=False):
		"""Helper to load configuration values from dictionary"""
		if do_debug:
			logger.info(f"apply_dict(other=, source={source})")
		ct = 0
		if not new_values:
			logger.warning(f"No values for '{source}'")
			return ct
		for key, value in new_values.items():
			old_value = self.get(key)
			old_source = self.sources.get(key)
			if do_debug:
				logger.info(f" {key}:")
			if old_value:
				if do_debug:
					logger.info(f" <-- {old_value} ({old_source})")
			if do_debug:
				logger.info(f" --> {value} ({source})")
			self[key] = value
			self.sources[key] = source
			ct += 1
			# logger.info(f"Value from file '{file_value}' replaced '{value}' for key '{key}'")
		logger.info(f" Put {ct} values from '{source}' into configuration")
		return ct

	def apply_json_config_file(self, filename, do_debug=False):
		"""Helper to load configuration values from configuration file in json format"""
		if do_debug:
			logger.info(f"apply_json_config_file(filename={filename})")
		file = Path(filename)
		# Create a config file with defaults if none exists
		if not file.is_file():
			if do_debug:
				logger.info(f" Config file '{filename}' did not exist, skipping")
				logger.info(f" NOTE: current dir was: {os.getcwd()}")
			return False
		# Load config from file
		loaded_config = {}
		if not os.path.exists(filename):
			logger.error(f"ERROR: Could not find '{filename}'")
			return False
		with open(filename, "r") as json_file:
			if do_debug:
				logger.info(f" Loading config from '{filename}'")
			try:
				loaded_config = json.load(json_file)
				# logger.info(f"LOADED JSON: {pprint.pformat(loaded_config)}")
				self.apply_dict(loaded_config, filename, do_debug)
			except Exception as e:
				logger.error(f"\nParsing json from config file '{filename}' failed:\n{e}\n", exc_info=True)
				return False
		return True


	def apply_yaml_config_file(self, filename, do_debug=False):
		"""Helper to load configuration values from configuration file in yaml format"""
		if do_debug:
			logger.info(f"apply_yaml_config_file(filename={filename})")
		file = Path(filename)
		# Create a config file with defaults if none exists
		if not file.is_file():
			if do_debug:
				logger.info(f" Config file '{filename}' did not exist, skipping")
				logger.info(f" NOTE: current dir was: {os.getcwd()}")
			return False
		# Load config from file
		loaded_config = {}
		if not os.path.exists(filename):
			logger.error(f"ERROR: Could not find '{filename}'")
			return False
		with open(filename, "r") as json_file:
			if do_debug:
				logger.info(f" Loading config from '{filename}'")
			try:
				loaded_config = yaml.safe_load(json_file)
				# logger.info(f"LOADED YAML: {pprint.pformat(loaded_config)}")
				self.apply_dict(loaded_config, filename, do_debug)
			except Exception as e:
				logger.error(f"\nParsing yaml from config file '{filename}' failed:\n{e}\n", exc_info=True)
				return False
		return True


	def list_unchanged(self):
		""" List all variables that have not been changed from their default setting"""
		logger.info(f"Unchanged configurations options:")
		for key, value in defaults.items():
			if self.get(key) == value:
				logger.info(f"{key}={value}")

	def members(self):
		""" Return all members of the config"""
		ret = {}
		base = self  # .__class__
		for member in [attr for attr in dir(base) if not callable(getattr(base, attr)) and not attr.startswith("__")]:
			val = getattr(base, member)
			ret[member] = val
		return ret

	def redact_key(self, key, val, num=20, source="redact"):
		"""Redact the value of a key for security"""
		if source in ["default", "none"]:
			return val
		if any(x in key.lower() for x in ["secret", "pass", "pwd", "key", "psk"]):
			val = octomy.utils.redact(val, num)
		return val

	def __str__(self):
		"""Print intuitive overview of settings"""
		dict = self.members()
		ret = f"\n########## Configuration options for {self.__class__.__name__}:\n"
		order = {"none": {}, "default": {}}
		for key, val in dict.items():
			if self.sources != val:
				source = self.sources.get(key, "none")
				order[source] = order.get(source, {})
				order[source][key] = val
		for source, items in order.items():
			if len(items) > 0:
				ret += f"[{c.BLUE}{source}{c.ENDC}]\n"
				for key, val in items.items():
					vc = c.GREEN
					rv = self.redact_key(key, val)
					if val == unset:
						vc = c.RED
					if rv != val:
						vc += c.BOLD
					ret += f" {c.BLUE}+ {c.CYAN}{key} {c.ENDC}= {vc}{rv}{c.ENDC}\n"
		return ret

	def redacted_dict(self) -> dict:
		"""Return the full config with all values redacted for security"""
		out_dict = dict(self.members())
		for key, val in out_dict.items():
			out_dict[key] = self.redact_key(key, val)
		return out_dict

	def attrify(self):
		""" Convert all config values in the dictionart into attributes"""
		for key, val in self.items():
			# logger.debug(f" + {key} = {self.redact_key(key, val)}")
			setattr(self.__class__, key, val)



class DefaultOctomyConfig(OctomyConfig):

	def __init__(self):
		"""The default base configuration to be extended by actual configurations to be used"""
		super().__init__()
		self.update(defaults)
		self.sources = {k: "default" for k in self.keys()}


	def verify(self):
		"""Helper to check validity of configuration"""
		defkey = []
		for key in ["printful-api-key"]:
			if self.get(key, None) == defaults.get(key, None):
				defkey.append(key)
		if defkey:
			logger.warning(f"Config contains default values for the following keys: '{', '.join(defkey)}'\n        If there are any authentication error this might be the culprit.")

		# Printify needs printful-api-key base64 encoded, so do that now b64encode
		pak = self.get("printful-api-key", None)
		if pak:
			self["printful-api-key-base64"] = str(base64.urlsafe_b64encode(pak.encode("utf-8")).strip(), "utf-8")


@lru_cache()
def get_config() -> OctomyConfig:
	do_debug = False
	config = OctomyConfig()
	org_ok = config.apply_yaml_config_file("config/organization.yaml", do_debug)
	app_ok = config.apply_yaml_config_file("config/application.yaml", do_debug)
	ser_ok = config.apply_yaml_config_file("config/service.yaml", do_debug)
	loc_ok = config.apply_yaml_config_file("config/local_secrets.yaml", do_debug)
	if not all([org_ok, app_ok, ser_ok, loc_ok]):
		logger.warning(f"No config files found from cwd='{os.getcwd()}'")
	config.apply_environment_variables(do_debug)
	#config.verify()
	config.attrify()
	if True or do_debug:
		logger.info(config)
	return config
