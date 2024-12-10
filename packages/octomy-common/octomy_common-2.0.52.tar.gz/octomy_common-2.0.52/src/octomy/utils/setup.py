#   __ __                 ___        _            
#  |  \  \ ___  ___  ___ / __> ___ _| |_ _ _  ___ 
#  |     |/ ._>/ . |<_> |\__ \/ ._> | | | | || . \
#  |_|_|_|\___.\_. |<___|<___/\___. |_| `___||  _/
#              <___'                         |_|  

from setuptools import find_namespace_packages
import logging
import os
import pprint
import re
import sys
import inspect
import warnings

log_setup_once = False


def setup_logging(name=None, log_level=logging.INFO):
	"""Set up logging."""
	global log_setup_once
	if not log_setup_once:
		log_setup_once = True
		logging.basicConfig(level=log_level)
		fmt = "%(asctime)s %(levelname)s (%(threadName)s) [%(name)s:%(lineno)s::%(funcName)s()] - %(message)s"
		colorfmt = "%(log_color)s{}%(reset)s".format(fmt)
		datefmt = "%Y-%m-%d %H:%M:%S"

		# Suppress overly verbose output that isn't helpful from some libraries we depend on
		for key in ["requests", "tensorboard", "urllib3", "aiohttp.access", "uamqp", "sqlalchemy", "sqlalchemy.engine.base", "matplotlib.font_manager"]:
			logging.getLogger(key).setLevel(logging.WARNING)

		# Enable debug logging for some insteresting libraries (for development)
		logging.getLogger("fk").setLevel(logging.DEBUG)

		try:
			from colorlog import ColoredFormatter

			logging.getLogger().handlers[0].setFormatter(ColoredFormatter(colorfmt, datefmt=datefmt, reset=True, log_colors={"DEBUG": "cyan", "INFO": "green", "WARNING": "yellow", "ERROR": "red", "CRITICAL": "red"}))
		except ImportError:
			# Ignore failures in loading color coded logs
			pass

		# Set this log level as default
		logger = logging.getLogger("")
		logger.setLevel(log_level)
	if not name:
		name = inspect.stack()[1][1]
	logger = logging.getLogger(name)
	try:
		import colored_traceback.auto
	except ImportError:
		pass

	return logger


logger = setup_logging(__name__)


def read_file(cwd:str, fname:str, strip:bool = True):
	fn = os.path.realpath(os.path.join(cwd, fname))
	data = ""
	if os.path.exists(fn):
		with open(fn) as f:
			data = f.read()
			data = data.strip() if strip else data
			# logger.info(f"Got data '{data}' from '{fn}'")
	else:
		logger.error(f"Could not find file {fn}")
		logger.warning(f"NOTE: Current working directory is {os.getcwd()}")
	return data


def write_file(cwd:str, fname:str, data:str, do_overwrite:bool = False):
	fn = os.path.realpath(os.path.join(cwd, fname))
	if not os.path.exists(fn) or do_overwrite:
		with open(fn, "w") as f:
			f.write(data)
	else:
		logger.warning(f"File {fn} already exists")
		logger.warning(f"NOTE: Current working directory is {os.getcwd()}")
	return data


def remove_comment(line, sep="#"):
	i = line.find(sep)
	if i >= 0:
		line = line[:i]
	return line.strip()


def read_requirements_file(cwd:str, fname:str, do_strip:bool = True, do_debug:bool = False):
	fn = os.path.realpath(os.path.join(cwd, fname))
	if do_debug:
		logger.info(f"Reading requirements from {fn} with do_strip = {do_strip}")
	lines = []
	if os.path.exists(fn):
		with open(fn) as f:
			for r in f.readlines():
				r = r.strip()
				if len(r) < 1:
					continue
				r = remove_comment(r)
				if len(r) < 1:
					continue
				lines.append(r)
	else:
		logger.error(f"Could not find requirements file {fn}")
		logger.warning(f"NOTE: Current working directory is {os.getcwd()}")
	# logger.warning(f"Full content of '{fname}' was: \n{lines}")
	if not do_strip:
		return lines
	out = []
	for line in lines:
		if line and not line.startswith("-"):
			out.append(line)
	return out


def debug_repo(repo):
	if not repo:
		logger.info(f"No repo")
		return
	logger.info(f"Repository head commit: {repo.head.commit}")
	logger.info(f"Found {len(repo.branches)} branches:")
	for branch in repo.branches:
		logger.info(f" + {branch}({branch.commit})")
	remote = repo.remote()
	logger.info(f"Found {len(remote.refs)} remote refs:")
	for ref in remote.refs:
		logger.info(f" + {ref}({ref.commit})")


def get_git_branch_from_env():
	branch_env = "FK_GIT_ACTUAL_BRANCH"
	branch = os.environ.get(branch_env, None)
	if branch is not None:
		logger.info(f"Using {branch_env} = {branch} from environment")
	else:
		logger.info(f"No value for {branch_env} found")
	return branch

def get_license_name(cwd:str, fname:str, do_debug:bool = False):
	fn = os.path.realpath(os.path.join(cwd, fname))
	if do_debug:
		logger.info(f"Reading license from {fn}")
	if os.path.exists(fn):
		with open(fn) as f:
			for r in f.readlines():
				r = r.strip()
				if len(r) < 1:
					continue
				# Return first non-empty line
				return r
	else:
		logger.error(f"Could not find license file {fn}")
		logger.warning(f"NOTE: Current working directory is {os.getcwd()}")
	return "Proprietary" # Fall back to something safe


def generate_version_string(version:str = None, branch:str = None):
	version = read_file(version_file) if version is None else version
	branch = get_git_branch_from_env() if branch is None else branch
	full_version = ""

	if branch == "production":
		full_version = version
	elif branch == "beta":
		full_version = f"{version}-beta"
	elif branch.startswith("stage-") and len(branch) > 6:
		full_version = f"{version}-{branch[6:]}"
	else:
		full_version = f"{version}-test-{branch.replace(' ','_').replace('	','_')}"
	logger.info(f"Using full version = {full_version}")
	return full_version


def generate_development_status(cwd:str, version:str = None, branch:str = None):
	version = read_file(cwd, version_file) if version is None else version
	branch = get_git_branch_from_env() if branch is None else branch
	development_status = ""
	# Calculate the development status based on current branch and bare version
	if branch == release_branch:
		development_status = "Development Status :: 5 - Production/Stable"
	elif branch == beta_branch:
		development_status = "Development Status :: 4 - Beta"
	elif "feature-" in branch:
		development_status = "Development Status :: 3 - Alpha"
	else:
		development_status = "Development Status :: 1 - Planning"
	return development_status


def get_development_status():
	# Not viable
	# return generate_development_status();
	return "Development Status :: 1 - Planning"

def find_packages(package_dir:str, modules:list, do_debug:bool = False):
	#return find_namespace_packages(where=package_dir, include=[module + ".*" for module in modules])
	includes = list()
	for module in modules:
		if do_debug:
			logger.info(f"Searching {module} for includes..")
		includes.append(module + ".*")
	if do_debug:
		logger.info(f"Includes found: {pprint.pformat(includes)}")
	found_packages = find_namespace_packages(where=package_dir, include=includes)
	if do_debug:
		logger.info(f"Packages found: {pprint.pformat(found_packages)}")
	return found_packages


# Function to recursively list all files in a directory
def list_files(directory:str, base:str):
	paths = list()
	for (path, directories, filenames) in os.walk(directory):
		for filename in filenames:
			paths.append(os.path.relpath(os.path.join(path, filename), base))
	return paths

def get_package_data(extensions:list, modules:list, package_dir:str, do_debug):
	out = dict()
	if do_debug:
		logger.info(f"get_package_data(extensions={extensions}, modules={modules}, package_dir={package_dir})")
	data_filters = list()
	for extension in extensions:
		data_filters.append(re.compile(fr'.*/{extension}(?:/{extension})*/[^/]+\.{extension}$'))
	for module in modules:
		modules_data_files = list_files(module, os.path.join(package_dir))
		data_files = list()
		for data_file in modules_data_files:
			for data_filter in data_filters:
				if data_filter.match(data_file):
					data_files.append(data_file)
					p = os.path.dirname(data_file)
					f = os.path.basename(data_file)
					m = ".".join(p.split("/"))
					ms = out.get(m, list())
					ms.append(f)
					out[m] = ms
					#logger.info(f"########## FOUND: {data_file}    (p={p}, f={f}, m={m})")
					break

	logger.info("Datafiles:---")
	logger.info(pprint.pformat(out))
	logger.info("-------------")
	return out

def clean_module_folder_name(dash_name):
	return dash_name.replace('-', '_')

# From https://pypi.org/pypi?%3Aaction=list_classifiers
def get_classifiers(python_version:str):
	return [
		  get_development_status()
		, "Intended Audience :: Developers"
		, "Intended Audience :: Information Technology"
		, "Intended Audience :: Science/Research"
		, "Intended Audience :: Other Audience"
		, "Topic :: Utilities"
		, "Natural Language :: English"
		, "Operating System :: POSIX :: Linux"
		, "Programming Language :: Python :: " + python_version
		, "Topic :: Other/Nonlisted Topic"
	]

def megasetup(source_data:dict):
	do_debug = source_data.get("debug", False)
	base_name = source_data.get("base_name")
	data_extensions = source_data.get("data_extensions", ['sql'])
	modules = set(source_data.get("modules", set()))
	additional_modules = source_data.get("additional_modules", list())
	group_base_name = source_data.get("group_base_name")
	package_dir = source_data.get("package_dir", "src")
	cwd = source_data.get("cwd", os.path.realpath(os.path.dirname(os.path.abspath(__file__))) )
	has_cli = source_data.get("has_cli", False)
	executable_name = source_data.get("executable_name")
	executable_package = source_data.get("executable_package")
	executable_package_path = source_data.get("executable_package_path")
	python_version = source_data.get("python_version", "3.10")
	version_file = "./VERSION"
	readme_file = "./README.md"
	license_file = "./LICENSE"
	
	if group_base_name:
		if len(modules) < 1:
			modules.add(clean_module_folder_name(group_base_name))
	modules.update(additional_modules)
	modules = list(modules)
	url = f"https://gitlab.com/{group_base_name}/{base_name}"
	scripts = list()
	entry_points = dict()
	if do_debug:
		logger.info(f"MEGASETUP       base_name: {base_name}")
		logger.info(f"                      cwd: {cwd}")
		logger.info(f"          data_extensions: {data_extensions}")
		logger.info(f"          group_base_name: {group_base_name}")
		logger.info(f"                  has_cli: {has_cli}")
		logger.info(f"             license_file: {license_file}")
		logger.info(f"                  modules: {modules}")
		logger.info(f"              package_dir: {package_dir}")
		logger.info(f"           python_version: {python_version}")
		logger.info(f"              readme_file: {readme_file}")
		logger.info(f"                      url: {url}")
		logger.info(f"             version_file: {version_file}")
	if has_cli or executable_name or executable_package or executable_package_path:
		executable_name = executable_name or base_name
		if not executable_package_path:
			executable_package_path=[clean_module_folder_name(group_base_name)]
			if executable_package:
				executable_package_path.append(executable_package)
			executable_package_path = '.'.join(executable_package_path)
		executable = f"{executable_name} = {executable_package_path}.cli:main"
		if executable_name:
			entry_points={"console_scripts": [executable]}

	package_data = get_package_data(data_extensions, modules, package_dir, do_debug)

	defaults_data = {
		  "author_email": "pypi@octomy.org"
		, "author_name": "OctoMY"
		, "beta_branch": "beta"
		, "changelog_file": "./CHANGELOG"
		, "classifiers": get_classifiers(python_version)
		, "entry_points": entry_points
		, "include_package_data": True
		# Allow flexible deps for install
		, "install_requires": read_requirements_file(cwd, "requirements/requirements.in", do_debug=do_debug)
		, "keywords": ["software"]
		, "license_files": (license_file,)
		, "license_name": get_license_name(cwd, license_file, do_debug=do_debug)
		, "long_description": read_file(cwd, readme_file)
		, "long_description_content_type": "text/markdown"
		# We use namespace packages to allow multiple packages to use the same package prefix
		# We omit __init__.py to accomplish this
		# See https://packaging.python.org/en/latest/guides/packaging-namespace-packages/
		, "modules": modules
		# NOTE: "data_files" is deprecated
		# NOTE: "package_data" need to reside inside a package, in other words a directory with __init__.py
		, "package_data": package_data
		, "package_dir": {'': package_dir}
		, "package_name": f"{group_base_name}_{base_name}" # see PEP625 https://peps.python.org/pep-0625/
		, "packages": find_packages(package_dir, modules)
		, "platforms": ["Linux"]
		, "project_urls": {"Docs": f"{url}//-/blob/production/README.md", "Bugs": f"{url}/issues", "C.I.": f"{url}/pipelines"}
		, "python_requires": ">=" + python_version
		, "scripts": scripts
		, "python_version": python_version
		, "release_branch": "development"
		, "setup_requirements": ["pytest-runner", "setuptools_scm", "python-dateutil"]
		, "short_description": f"{group_base_name}/{base_name}"
#		, "test_suite": os.path.join(package_dir, "tests")
		# Use flexible deps for testing
		, "tests_require": read_requirements_file(cwd, "requirements/test_requirements.in", do_debug=do_debug)
		, "url": url
		, "version_string": read_file(cwd, version_file)
		, "zip_safe": True
	}

	for key, value in defaults_data.items():
		source_data.setdefault(key, value)



	package = {
		  "author": source_data.get("author_name")
		, "author_email": source_data.get("author_email")
		, "classifiers": source_data.get("classifiers")
		, "description": source_data.get("short_description")
		, "entry_points": source_data.get("entry_points")
		, "include_package_data": source_data.get("include_package_data")
		, "install_requires": source_data.get("install_requires")
		, "keywords": ", ".join(source_data.get("keywords", []))
		, "license": source_data.get("license_name")
		, "license_files": source_data.get("license_files")
		, "long_description": source_data.get("long_description")
		, "long_description_content_type": source_data.get("long_description_content_type")
		, "maintainer": source_data.get("author_name")
		, "maintainer_email": source_data.get("author_email")
		, "name": source_data.get("package_name")
		, "namespace_packages": source_data.get("modules")
		, "package_data": source_data.get("package_data")
		, "package_dir": source_data.get("package_dir")
		, "packages": source_data.get("packages", list())
		, "platforms": source_data.get("platforms")
		, "project_urls": source_data.get("project_urls")
		, "python_requires": source_data.get("python_requires")
		, "setup_requires": source_data.get("setup_requirements")
#		, "test_suite": source_data.get("test_suite") # Deprecated
#		, "tests_require": source_data.get("tests_require")
		, "url": source_data.get("url")
		, "version": source_data.get("version_string")
		, "zip_safe": source_data.get("zip_safe")
#		, "scripts": source_data.get("scripts") #Using entry_points instead
	}
	#del package['package_data']
	for key,val in package.items():
		if not val:
			logger.info(f" {key}:{val}  <-- EMPTY ¤ ¤ ¤ ¤ ¤ ¤ ¤ ¤")
		else:
			logger.info(f" {key}:{len(str(val))} bytes")
	if do_debug:
		logger.info("-------------------------------------------------------")
		logger.info("'  setup.py package:")
		logger.info(pprint.pformat(package))
		logger.info("-------------------------------------------------------")
	return package
