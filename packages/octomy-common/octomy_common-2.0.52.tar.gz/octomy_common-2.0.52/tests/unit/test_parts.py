import logging
import octomy.db
import octomy.web.context
import octomy.cad.parts
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
async def test_parts():
	#parts = octomy.cad.parts.Parts()
	pass

