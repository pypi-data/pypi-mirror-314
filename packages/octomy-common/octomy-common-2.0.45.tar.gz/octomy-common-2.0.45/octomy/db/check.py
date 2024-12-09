import datetime
import logging
import octomy.config
import octomy.db
import pydantic

logger = logging.getLogger(__name__)



class DbTime(pydantic.BaseModel):
	now:datetime.datetime

class DatabaseCheck:
	def __init__(self, config):
		config:octomy.config.OctomyConfig = octomy.config.get_config()
		self.dbc:octomy.db.Database = octomy.db.get_database(config)
		assert self.dbc.is_ok()
		self.create_tables()


	# Get current time from db
	def get_now(self, do_debug=False) -> DbTime, str|None:
		db_ret, db_err = await self.dbc.query_One("octomy.db.get_now", params=dict(), item_type=DbTime, prepare=False, do_debug=do_debug)
		return db_ret, db_err
 

	def verify(self):
		try:
			db_ret, db_err = self.get_now()
			return None == db_err
		except Exception as e:
			logger.warning(f"Unknown error '{e}':", exc_info=True)
			return False
