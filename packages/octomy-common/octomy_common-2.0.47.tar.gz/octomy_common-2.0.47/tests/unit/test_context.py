import logging
import octomy.db
import octomy.web.context
import os
import pprint
import pytest
import datetime


logger = logging.getLogger(__name__)

# fmt: off
dummy_config= {
	"db-hostname":"hello.com"
	,"db-port":"1234"
	,"db-username":"arnold"
	,"db-password":"secret123"
	,"db-database":"mydb"
}
# fmt: on



@pytest.mark.asyncio
async def test_get_context():
	context = octomy.web.context.get_context()
	context = octomy.web.context.get_context(required_scopes = list())
	
	optional_key = "optional_key"
	optional_data = "optional_data"
	'''
	data:Data = Data()
	parts:Parts = Parts()
	search_engine:SearchEngine = SearchEngine()
	data:Data = None
	parts:Parts = None
	search_engine:SearchEngine = None
	'''
	outcome = None
	try:
		outcome = context.optional_key
	except:
		pass
	assert None is outcome, "optional_key should not be set at this point"
	outcome = None
	context.set_optional_attribute(optional_key, optional_data)
	try:
		outcome = context.optional_key
	except:
		pass
	assert optional_data is outcome, f"optional_key should be set to '{optional_data}' at this point"

