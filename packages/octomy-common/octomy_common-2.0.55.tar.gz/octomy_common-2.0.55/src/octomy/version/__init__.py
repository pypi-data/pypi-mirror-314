import os
import pkg_resources
from octomy.utils import get_package_file_content

import logging

logger = logging.getLogger(__name__)


version_filename = "VERSION"


def get_version(pkg):
	return get_package_file_content(pkg, version_filename) or "0.0.0"
