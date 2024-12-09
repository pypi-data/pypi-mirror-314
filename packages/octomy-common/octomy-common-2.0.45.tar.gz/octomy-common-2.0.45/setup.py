#!/usr/bin/env python
import logging
import os
import pprint
from setuptools import setup

logger = logging.getLogger(__name__)


source_data = {
	  "base_name": "common"
	, "group_base_name": "octomy"
	, "cwd": os.path.dirname(os.path.abspath(__file__))
	, "debug": True
}

package = dict()
try:
	from octomy.utils.setup import megasetup
	package = megasetup(source_data = source_data)
except:
	from .octomy.utils.setup import megasetup
	package = megasetup(source_data = source_data)

setup(**package)
