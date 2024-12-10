import logging
from furl import furl
import fk.utils

logger = logging.getLogger(__name__)

def config_to_url(config, do_redact=False):
	if not config:
		return ""
	db_hostname = config.get("db-hostname", None)
	db_port = config.get("db-port", None)
	db_username = config.get("db-username", None)
	db_password = config.get("db-password", None)
	db_database = config.get("db-database", None)
	if do_redact:
		db_password = fk.utils.redact(db_password)
	f = furl()
	f.set(scheme="postgres", username=db_username, password=db_password, host=db_hostname, port=db_port, path=db_database)
	return f.url


def url_to_config(db_url):
	f = furl(db_url)
	if f.scheme != "postgres":
		logger.warning("db_url URL did not have postgres scheme")
		return {}
	database = (f.path.segments or [""])[0]
	# fmt:off
	config={
	  "db-hostname": f.host
	, "db-port": f.port
	, "db-username": f.username
	, "db-password": f.password
	, "db-database": database
	}
	# fmt:on
	return config


def get_config_hash(config):
	if not config:
		return ""
	key = ""
	for i in ["hostname", "port", "username", "password", "database"]:
		key += fk.utils.hashstr(config.get(f"db-{i}", ""))
	return fk.utils.hashstr(key)
