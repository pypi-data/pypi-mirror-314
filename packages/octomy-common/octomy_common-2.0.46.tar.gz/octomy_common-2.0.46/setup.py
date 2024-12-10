#!/usr/bin/env python
from setuptools import setup
import logging
import os
import pprint
import sys

source_data = {
	  "base_name": "common"
	, "group_base_name": "octomy"
	, "cwd": os.path.dirname(os.path.abspath(__file__))
	, "debug": True
}

ms = None
sl = None

try:
	#project_path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
	#sys.path.insert(0, project_path)
	#print(f"balls:{project_path}")
	from octomy.utils.setup import megasetup, setup_logging
	ms = megasetup
	sl = setup_logging
except Exception as e:
	print(" ")
	print("^^^^^^^^^^^^^^^^^^^^^^^")
	print(f"Megasetup not available: {e}")
	print("^^^^^^^^^^^^^^^^^^^^^^^")
	print(" ")
	sys.exit(1)

logger = sl(__name__)


logger.info("source_data")
logger.info(pprint.pformat(source_data))

try:
	package = ms(source_data = source_data)
	logger.info("package:")
	logger.info(pprint.pformat(package))
	logger.info("setup():")
	setup(**package)
except Exception as e:
	logger.error(f"Error during megasetup: {e}")
	logger.exception(e)

