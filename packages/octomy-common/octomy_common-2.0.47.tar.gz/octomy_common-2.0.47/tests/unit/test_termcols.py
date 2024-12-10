import logging
import octomy.utils
import os
import pprint
import pytest
import datetime


logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def _test_termcols():
	for name, color in vars(octomy.utils.termcol).items():
		if not name.startswith('__') and isinstance(color, str):
			bare = color.replace(octomy.utils.colbase, '')
			logger.info(f"{color}{name}\033[0m  {bare}")
