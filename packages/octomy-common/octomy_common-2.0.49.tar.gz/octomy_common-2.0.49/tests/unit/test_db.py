import logging
import octomy.db
import os
import pprint
import pytest


logger = logging.getLogger(__name__)


here = os.path.dirname(__file__)
data_dir = os.path.join(here, "data")


# fmt: off
dummy_config= {
	"db-hostname":"hello.com"
	,"db-port":"1234"
	,"db-username":"arnold"
	,"db-password":"secret123"
	,"db-database":"mydb"
}
# fmt: on


def _test_db_get_same_twice():
	dbc1, err = octomy.db.get_database(config)
	dbc2, err = octomy.db.get_database(config)
	assert dbc1 == dbc2


@pytest.mark.asyncio
async def _test_get_database():
	config = {}
	dbc, err = octomy.db.get_database(config)
	assert(not dbc)
	assert(err)
	logger.warning(err)
	
	config = {
		'db-username': "test"
	}
	dbc, err = octomy.db.get_database(config)
	assert(not dbc)
	assert(err)
	logger.info(err)
	
	config = {
		'db-username': 1234
	}
	dbc, err = octomy.db.get_database(config)
	assert(not dbc)
	assert(err)
	logger.info(err)


	config = {
		  'db-username': "test"
		, 'db-port': "test"
	}
	dbc, err = octomy.db.get_database(config)
	assert(not dbc)
	assert(err)
	logger.info(err)
	
	config = {
		  'db-hostname': "test"
		, 'db-username': "test"
	}
	dbc, err = octomy.db.get_database(config)
	assert(not dbc)
	assert(err)
	logger.info(err)
	
	config = {
		  'db-hostname': "test"
		, 'db-username': "test"
		, 'db-password': "test"
	}
	dbc, err = octomy.db.get_database(config)
	assert(not dbc)
	assert(err)
	logger.info(err)
	
	config = {
		  'db-hostname': "test"
		, 'db-username': "test"
		, 'db-password': "test"
		, 'db-database': "test"
	}
	dbc, err = octomy.db.get_database(config, do_online=False)
	assert dbc, err
	assert not err, err
	logger.info(err)

	config = {
		  'db-hostname': "test"
		, 'db-username': "test"
		, 'db-password': "test"
		, 'db-database': "test"
	}
	dbc, err = octomy.db.get_database(config, do_online=True)
	assert not dbc, "Should fail"
	assert err, "Should fail"
	logger.info(err)




@pytest.mark.asyncio
async def _test_db():
	logger.info(f"here:{here}, data_dir:{data_dir}")
	config = {
		  'db-hostname': os.environ.get("TEST_DB_HOSTNAME")
		, 'db-port':     os.environ.get("TEST_DB_PORT")
		, 'db-database': os.environ.get("TEST_DB_DATABASE")
		, 'db-username': os.environ.get("TEST_DB_USERNAME")
		, 'db-password': os.environ.get("TEST_DB_PASSWORD")
	}
	db, err = octomy.db.get_database(config, )
	assert db, err
	# await db.preload_queries(f"{data_dir}/sql/")
	my_uuid = str(uuid.uuid4())
	# Assuming 'access.users.upsert' is a valid key and 'user_data' is a dictionary with the necessary parameters
	output=dict()
	matrix = [
		{
			  "query_key":"access.users.upsert"
			, "mode":"none"
			, "expected_result":None
			, "expected_error": 'query parameter missing: data, email, enabled'
			, "params": {'id': 1, 'name': 'John Doe'}
		}
		, {
			  "query_key":"access.users.upsert"
			, "mode": "one"
			, "expected_result": None
			, "expected_error": None
			, 'output_key': "my_id"
			, "params": {'id': 1, 'name': 'John Doe', 'data': 'balls', 'email': 'lolbob@sulla.com', 'enabled': True}
		}
	]
	for case in matrix:
		query_key = case.get("query_key")
		expected_result = case.get("expected_result")
		expected_error = case.get("expected_error")
		params = case.get("params")
		mode = case.get("mode", "none")
		logger.info(f"CASE query_key={query_key} expected_result={expected_result} expected_error={expected_error} params={params} mode={mode}")
		if mode == "none":
			actual_result, actual_error = await db.query_none(query_key = query_key, params=params)
		elif mode == "one":
			actual_result, actual_error = await db.query_one(query_key = query_key, params=params)
		elif mode == "many":
			actual_result, actual_error = await db.query_many(query_key = query_key, params=params)
		elif mode == "exists":
			actual_result, actual_error = await db.query_exists(query_key = query_key, params=params)
		else:
			raise Exception("incorrect mode. TODO: handle in testing")
		logger.info("EXPECTED RESULT:")
		logger.info(pprint.pformat(expected_result))
		logger.info("ACTUAL RESULT:")
		logger.info(pprint.pformat(actual_result))
		logger.info("EXPECTED ERROR:")
		logger.info(pprint.pformat(expected_error))
		logger.info("ACTUAL ERROR:")
		logger.info(pprint.pformat(actual_error))
		assert(actual_result == expected_result)
		assert(actual_error == expected_error)


def _test_query_key_to_sql_path():
	query_key = "octomy.db.get_now"
	logger.info(f"             query_key:{query_key}")
	sql_path = octomy.db.query_key_to_sql_path(query_key = query_key, relative=False, do_debug=True)
	logger.info(f"              sql_path:{sql_path}")
	assert bool(sql_path)
	assert os.path.exists(sql_path)



@pytest.mark.asyncio
async def test_convert_params():
	import pydantic #import BaseModel, StringConstraints, HttpUrl, validator
	import typing #import List, Optional, Annotated, Any, Dict
	class TestType(pydantic.BaseModel):
		test_str:str = "test str"
		test_constrained: typing.Annotated[str, pydantic.StringConstraints(max_length=255)] | None = None
		test_int:int = 1337
		test_bool:bool = True
		test_url:pydantic.HttpUrl = pydantic.HttpUrl("https://example.com:8888/somepath/endpoint?query1=lol#fragment")
	params_type = TestType()
	params_dict = octomy.db.pydantic_to_params(params_type)
	logger.info(f"FROM pydantic: {pprint.pformat(params_type)}")
	logger.info(f"TO params: {pprint.pformat(params_dict)}")
	
@pytest.mark.asyncio
async def _test_sql():
	config = {
		  'db-hostname': "test"
		, 'db-username': "test"
		, 'db-password': "test"
		, 'db-database': "test"
	}
	dbc, err = octomy.db.get_database(config, do_online=False)
	assert dbc, err
	assert not err, err
	query_key = "octomy.db.get_now"
	query = await dbc.load_query(query_key=query_key, do_debug=True)
	logger.info(f"query:'{query}'")
	assert bool(query), f"No query found for {query_key}"
