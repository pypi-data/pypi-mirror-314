from dotenv import dotenv_values
from octomy.cad import openscad
import datetime
import logging
import os
import pprint
import pytest
import re
import shutil

logger = logging.getLogger(__name__)




here = os.path.dirname(__file__)
data_dir = os.path.join(here, "data")
env = dict()
env_re = re.compile(r'export (?P<key>.*)=(?P<value>.*)')


def parse_env(here):
	env_file = os.path.join(here, ".env")
	return dotenv_values(env_file)

def parse_env_old(here):
	env_file = os.path.join(here, ".env")
	out = dict()
	if os.path.isfile(env_file):
		with open(env_file, "r") as f:
			data = f.read()
			#logger.info(f"data: {data}")
			for m in env_re.finditer(data):
				gd = m.groupdict()
				#logger.info(f"gd: {gd}")
				out[gd.get('key')] = gd.get('value')
				#logger.info(f"line: {gd.get('key')} = {gd.get('value')}")
	else:
		logger.warning(f"Could not find env file: {env_file}")
	return out


def get_env(key, fb=None):
	global env
	if env == {}:
		env = parse_env(here)
	ret = env.get(key) or os.environ.get(key) or fb
	logger.info(f"GOT {key}={ret}")
	return ret


def remove_dir(dir):
	logger.info(f"Removing dir '{dir}'")
	if os.path.isdir(dir):
		shutil.rmtree(dir, ignore_errors=True)
	assert(not os.path.isdir(dir))

"""
@pytest.fixture(scope='function')
def git_repo(request):
	logger.info(f"here:{here}, project_folder:{git_folder}")
	git_data = {
		  "path": "github.com/arribatec-cloud/small-test-repo.git"
		, "username": get_env("TEST_GIT_USERNAME", None)
		, "password": get_env("TEST_GIT_PASSWORD", None)
		, "do_debug": True
	}
	logger.info("creating client with:")
	logger.info(pprint.pformat(git_data))
	remove_dir(git_folder)
	repo = git.Client(**git_data)
	logger.info("creating client DONE")
	assert(repo)
	repo.state()
	def teardown():
		logger.info("TEARDONE")
		repo = None
		remove_dir(git_folder)
	request.addfinalizer(teardown)
	return repo
"""
