import json
import os
import sqlite3
import pprint
import psycopg
import traceback
import sys
import logging
from urllib.parse import urlparse, urlunparse, ParseResult
import pytz
import fk.utils
from .utils import config_to_url, get_config_hash
import unicodedata

import pprint

logger = logging.getLogger(__name__)


class DatabaseConnectionAsync:

    def __init__(self, config, event_source=None):
        self.config = config
        self.event_source=event_source
        self.db_hostname = self.config.get("db-hostname", None)
        self.db_port = self.config.get("db-port", None)
        self.db_username = self.config.get("db-username", None)
        self.db_password = self.config.get("db-password", None)
        self.db_database = self.config.get("db-database", None)
        self.db = None
        self.connstr = config_to_url(config, do_redact=False)
        connstr_safe= config_to_url(config, do_redact=True)
        logger.info(f"DATABASE(ASYNC): {connstr_safe}")
        self.pool=ConnectionPool(conninfo=self.connstr, open=not self.event_source, min_size=1, max_size = 100)
        if self.event_source:
            self.add_event_handler("startup", pool.open)
            self.add_event_handler("shutdown", pool.close)

        self.connection_error = None
        self._prepare_db()

    def __del____(self):
        self._unprepare_db()

    def is_ok(self):
        return self.db_hostname and self.db_port and self.db_username and self.db_password and self.db_database

    async def _unprepare_db(self):
        if self.db:
            try:
                # Make sure data is stored
                self.db.commit()
                self.db.close()
            except Exception as e1:
                pass
            try:
                del self.db
            except Exception as e2:
                pass
            self.db = None
            logger.info("PostgreSQL connection is closed")

    # Internal helper to connect to database
    async def _prepare_db(self):
        with await psycopg.AsyncConnection.connect(conninfo=self.connstr) as aconn:
           async with aconn.cursor() as acur:
               await acur.execute("SELECT now();")
               await acur.fetchone()
               async for record in acur:
                   logger.info(f"NOW ASYNC: {record}")

"""
            self.db = psycopg2.connect(host=self.db_hostname, port=self.db_port, user=self.db_username, password=self.db_password, database=self.db_database)

            # Create a cursor to let us work with the database
            with self.db:
                with self.db.cursor() as c:
                    # logger.info( self.db.get_dsn_parameters(),"\n")

                    c.execute("SELECT version();")
                    record = c.fetchone()
                    logger.info(f"Connected to: {record[0]}\n")
                    return True

        except (Exception, psycopg2.Error) as error:
            logger.warning("###   ###   ###   ###   ###   ###   ###   #")
            logger.warning("##   ###   ###   ###   ###   ###   ###   ##")
            logger.warning("")
            logger.warning(f"Error while connecting to PostgreSQL {error}")
            self.connection_error = error
            self._unprepare_db()
        return False

    async def reconnect(self):
        logger.info("###   ###   ###   ###   ###   ###   ###   #")
        logger.info("##   ###   ###   ###   ###   ###   ###   ##")
        logger.info("")
        logger.info(f"Reconnecting...")
        await self._unprepare_db()
        return await self._prepare_db()
"""
