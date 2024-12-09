from octomy.utils import get_package_relative_dir, get_package_root_dir, tree
import logging
import octomy.db
import os
import pprint

logger = logging.getLogger(__name__)

# fmt: off
configs = {
	"empty:":(
		{}
		,""
		,""
	)
	, "hello:":(
		{
			"db-hostname":"hello.com"
			,"db-port":1234
			,"db-username":"arnold"
			,"db-password":"secret123"
			,"db-database":"mydb"
		}
		,"F12F52B73358C297F47A80768ABDFADF20D021F6A20E9929178908F981B75FA1"
		,"postgres://arnold:secret123@hello.com:1234/mydb"
	)
}
# fmt: on


def _test_redact():
	min = 10
	base = "lorem ipsum dolor sit amet alla balla tralla lalla"
	l = len(base)
	for i in range(0, min*2):
		sub = ""
		for j in range(0, i):
			sub += base[ j % l ]
		redacted = octomy.utils.redact(sub, min)
		logger.info(f"{sub} --> {redacted}")

def _test_db_get_config_hash():

	for name, pack in configs.items():
		logger.info(f"NAME:{name}")
		config, expected, _ = pack
		logger.info(f"config:{config}")
		logger.info(f"expected:{expected}")
		actual = octomy.db.get_config_hash(config)
		logger.info(f"actual:{actual}")
		assert actual == expected
	return True


def _test_db_uri_to_and_from_config():
	for name, pack in configs.items():
		logger.info(f"NAME:{name}")
		expected_config, _, expected_uri = pack
		logger.info(f"expected_config:{expected_config}")
		logger.info(f"expected_uri:   {expected_uri}")
		actual_uri, actual_uri_err = octomy.db.db_uri_from_conf(expected_config, do_online=False)
		actual_config = octomy.db.db_uri_to_config(expected_uri, do_online=False)
		if None == actual_uri:
			logger.info(f"actual_uri_err={actual_uri_err}")
		else:
			assert actual_uri == expected_uri
			assert actual_config == expected_config

def _test_tree():
	path = get_package_relative_dir(True)
	logger.info(f"relpath: {path}")
	listing = tree(path.parent)
	logger.info(f"listing:\n{listing}")
	#tree()


def _test_stripes():
	#logger.info(stripes())
	matrix = [
		{
			  "expected_result": '\x1b[94m###   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###   #\x1b[0m\n\x1b[94m##   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###   ##\x1b[0m\n\x1b[94m#   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###\x1b[0m\n'
			, "params": {'cols':79, 'rows':3, 'on':3, 'off':3, 'on_char':"#", 'off_char':" ", 'offset':0, 'sheer':1}
		}
		, {
			  "expected_result": '\x1b[94m*-****-****-****-****-****-****-****-***\x1b[0m\n\x1b[94m-****-****-****-****-****-****-****-****\x1b[0m\n'
			, "params": {'cols':40, 'rows':2, 'on':4, 'off':1, 'on_char':"*", 'off_char':"-", 'offset':3, 'sheer':1}
		}
		, {
			  "expected_result": '\x1b[94m!%%!!%%!!%\x1b[0m\n\x1b[94m%%!!%%!!%%\x1b[0m\n\x1b[94m%!!%%!!%%!\x1b[0m\n\x1b[94m!!%%!!%%!!\x1b[0m\n\x1b[94m!%%!!%%!!%\x1b[0m\n\x1b[94m%%!!%%!!%%\x1b[0m\n\x1b[94m%!!%%!!%%!\x1b[0m\n\x1b[94m!!%%!!%%!!\x1b[0m\n\x1b[94m!%%!!%%!!%\x1b[0m\n\x1b[94m%%!!%%!!%%\x1b[0m\n'
			, "params": {'cols':10, 'rows':10, 'on':2, 'off':2, 'on_char':"%", 'off_char':"!", 'offset':3, 'sheer':1}
		}
	]
	for case in matrix:
		expected_result = case.get("expected_result")
		params = case.get("params")
		actual_result = octomy.utils.stripes(**params)
		logger.info(f"CASE expected_result={expected_result} params={params}")
		logger.info("EXPECTED RESULT:")
		logger.info(pprint.pformat(expected_result))
		logger.info("ACTUAL RESULT:")
		logger.info(pprint.pformat(actual_result))
		assert(actual_result == expected_result)


# fmt: off
query_key_test_cases = {
	"empty:":(
		  ""
		, None
	)
	, "long:":(
		  "octomy.batch.sub.dub.ding"
		, "octomy/batch/sub/dub/sql/ding.sql"
	)
}
# fmt: on

def _test_query_key_to_sql_path_relative():
	for name, pack in query_key_test_cases.items():
		query_key, expected = pack
		actual = octomy.db.query_key_to_sql_path(query_key = query_key, relative = True, do_debug = True)
		logger.info(f"NAME:{name}")
		logger.info(f"  query_key:{query_key}")
		logger.info(f"   expected:{expected}")
		logger.info(f"     actual:{actual}")
		assert actual == expected


def _test_get_package_root_dir():
	dir = get_package_root_dir()
	logger.info(f"get_package_root_dir:{dir}")


def _test_combined():
	package_dir = get_package_root_dir('octomy.utils')
	logger.info(f"  get_package_root_dir:{package_dir}")
	assert bool(package_dir)
	package_dir = package_dir.parent
	query_key = "octomy.db.get_now"
	logger.info(f"             query_key:{query_key}")
	sql_path = octomy.db.query_key_to_sql_path(query_key = query_key, relative = True, do_debug = True)
	logger.info(f"              sql_path:{sql_path}")
	assert sql_path == "octomy/db/sql/get_now.sql"
	canonical_path = os.path.join(package_dir, sql_path)
	logger.info(f"        canonical_path:{canonical_path}")
	assert bool(canonical_path)
	assert os.path.exists(canonical_path)




def _test_xray():
	
	bob = {
		  "alla":  [(1, 3), (3, 3), (1, "bob"), (3, 1), (5, 0), (4, 10)]
		, "balla":  ["lo", "bo", "ho"]
		, "sjokki": { "lol":123445, "bob":3452345.3455, "foo":"bar"}
		, "hehe": None
		, "hoho": False
	}
	
	ret = octomy.utils.xray(bob)


def _test_random_token():
	for i in range(0, 100):
		logger.info(octomy.utils.random_token(length=10))
