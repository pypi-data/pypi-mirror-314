from dateutil.relativedelta import relativedelta
from urllib.parse import urlparse
from uuid import UUID
import asyncio
import base64
import datetime
import hashlib
import importlib.util
import inspect
import json
import logging
import mmap
import os
import pathlib
import pkg_resources
import pprint
import random
import requests
import sys
import time
import string


logger = logging.getLogger(__name__)

# We want 4 second timeout for HTTP requests
HTTP_TIMEOUT = 4.0
_requests_session_instance = None

'''
	Name:				Code
	------				--------
'''
colbase = '\033'

class termcol:
	ENDC =				f'{colbase}[0m'
	RESET =				f'{colbase}[39m{colbase}[49m' #         - Reset color
	#CLEAR_LINE =		f'{colbase}[2K                          - Clear Line
	#MOVE_CURSOR = 		f'{colbase}[<L>;<C>H or \\033[<L>;<C>f  - Put the cursor at line L and column C.
	#XXX =				f'{colbase}[<N>A                        - Move the cursor up N lines
	#XXX =				f'{colbase}[<N>B                        - Move the cursor down N lines
	#XXX =				f'{colbase}[<N>C                        - Move the cursor forward N columns
	#XXX =				f'{colbase}[<N>D                        - Move the cursor backward N columns
	#CLEAR_SCREEN =		f'{colbase}[2J                          - Clear the screen, move to (0,0)
	#ERASE_TO_END_OF_LINE =			f'{colbase}[K               - Erase to end of line
	#SAVE_CURSOR =		f'{colbase}[s                           - Save cursor position
	#RESTORE_CURSOR =	f'{colbase}[u                           - Restore cursor position\n
	UNDERLINE_ON =		f'{colbase}[4m' #                       - Underline on
	UNDERLINE_OFF =		f'{colbase}[24m' #                      - Underline off
	BOLD_ON =			f'{colbase}[1m' #                       - Bold on
	BOLD_OFF =			f'{colbase}[21m' #                      - Bold off
	
	
	#ORANGE = f'{colbase}[94m'
	DEFAULT =			f'{colbase}[39m'
	BLACK =				f'{colbase}[30m'
	DARK_RED =			f'{colbase}[31m'
	DARK_GREEN =		f'{colbase}[32m'
	DARK_YELLOW =		f'{colbase}[33m'
	ORANGE =			f'{colbase}[33m' # Helper
	DARK_BLUE =			f'{colbase}[34m'
	DARK_MAGENTA =		f'{colbase}[35m'
	DARK_CYAN =			f'{colbase}[36m'
	LIGHT_GRAY =		f'{colbase}[37m'
	DARK_GRAY =			f'{colbase}[90m'
	RED =				f'{colbase}[91m'
	GREEN =				f'{colbase}[92m'
	YELLOW =			f'{colbase}[93m'
	BLUE =				f'{colbase}[94m'
	MAGENTA =			f'{colbase}[95m'
	PURPLE =			f'{colbase}[95m' # Helper
	CYAN =				f'{colbase}[96m'
	WHITE =				f'{colbase}[97m'
	BG_DEFAULT =		f'{colbase}[49m'
	BG_BLACK =			f'{colbase}[40m'
	BG_DARK_RED =		f'{colbase}[41m'
	BG_DARK_GREEN =		f'{colbase}[42m'
	BG_DARK_YELLOW =	f'{colbase}[43m'
	BG_DARK_BLUE =		f'{colbase}[44m'
	BG_DARK_MAGENTA =	f'{colbase}[45m'
	BG_DARK_CYAN =		f'{colbase}[46m'
	BG_LIGHT_GRAY =		f'{colbase}[47m'
	BG_DARK_GRAY =		f'{colbase}[100m'
	BG_RED =			f'{colbase}[101m'
	BG_GREEN =			f'{colbase}[101m'
	BG_ORANGE =			f'{colbase}[103m'
	BG_BLUE =			f'{colbase}[104m'
	BG_MAGENTA =		f'{colbase}[105m'
	BG_CYAN =			f'{colbase}[106m'
	BG_WHITE =			f'{colbase}[107m'


def redact(val, minimum=20):
	total = len(val)
	scramble_n = max(minimum, total - 3)
	show_n = max(min(total - minimum, 3), 0)
	out = val[0:show_n] + "*" * (scramble_n)
	return out


def file_contains_str(filename, str):
	return file_contains_bytes(filename, str.encode("utf-8"))


def file_contains_bytes(filename, bytes):
	# mmap does not work for empty files
	if os.stat(filename).st_size == 0:
		return False
	with open(filename, "rb", 0) as file, mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
		if s.find(bytes) != -1:
			return True
	return False


# Merge two dictionaries
def merge(dict1, dict2):
	res = {**dict1, **dict2}
	return res


# Determine if given URL is valid
def is_url_valid(url):
	try:
		result = urlparse(url)
		# 		if not result.scheme:
		# 			print ("No scheme")
		# 		if not result.netloc:
		# 			print ("No netloc")
		# 		if not result.path:
		# 			print ("No path")
		# 		if not result.scheme in ['http', 'https']:
		# 			print ("Scheme invalid")

		return all([result.scheme, result.netloc]) and result.scheme in ["http", "https"]
		# result.netloc,
	except:
		return False


def is_valid_uuid(uuid_to_test, version=4):
	"""
	Check if uuid_to_test is a valid UUID.

	Parameters
	----------
	uuid_to_test : str
	version : {1, 2, 3, 4}

	Returns
	-------
	`True` if uuid_to_test is a valid UUID, otherwise `False`.

	Examples
	--------
	>>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
	True
	>>> is_valid_uuid('c9bf9e58')
	False
	"""
	try:
		uuid_obj = UUID(uuid_to_test, version=version)
	except ValueError:
		return False

	return str(uuid_obj) == uuid_to_test


# Create a hash hex digest from string
def hashstr(raw):
	if type(raw) != type(""):
		raw = f"{raw}"
	sha256 = hashlib.sha256()
	sha256.update(raw.encode("utf-8"))
	return sha256.hexdigest().upper()


def hashfile(fn):
	file = open(fn, "r+")
	size = os.path.getsize(fn)
	sha256 = hashlib.sha256()
	sha256.update(mmap.mmap(file.fileno(), size))
	return sha256.update(mmap.mmap(file.fileno(), size))


# Turn invalid string into naive URL by prepending schema and appending path
def decorate_url(url):
	if not is_url_valid(url):
		url = "http://{url}/".format(url=url)
	return url


# Return dict with url split into components as appropriate for storing in database
def split_url(url_full):
	ret = {"url_hostname": "", "url_schema": "", "url_path": "", "url_query": "", "url_fragment": ""}
	try:
		parts = urlparse(url_full)
		if parts.netloc is not None:
			ret["url_hostname"] = parts.netloc
		if parts.scheme is not None:
			ret["url_schema"] = parts.scheme
		if parts.path is not None:
			ret["url_path"] = parts.path
		if parts.query is not None:
			ret["url_query"] = parts.query
		if parts.port is not None:
			ret["url_port"] = parts.port
		if parts.fragment is not None:
			ret["url_fragment"] = parts.fragment
	except Exception as e:
		# print(f"ERROR SPLITTING URL: {e}")
		pass
	return ret


def flatten_headers(headers):
	out = ""
	for k, v in headers.items():
		out += f"'{k}'='{v}'\n"
	return out


def verify_input_files(input_options):
	input_files = []
	notes = []
	if input_options:
		for file in input_options:
			note = "[OK]"
			if not os.path.exists(file):
				note = "[MISSING, Skipped]"
			elif not os.path.isfile(file):
				note = "[NOT A FILE, Skipped]"
			elif os.access(file, os.R_OK):
				note = "[NOT READABLE, Skipped]"
			else:
				input_files.append(file)
			notes.append(f' "{file}"   {note}')
		return input_files, notes
	else:
		return None, None


def verify_output_file(output_file):
	valid_output_file = None
	if output_file:
		output_path = os.path.dirname(os.path.realpath(output_file))
		os.makedirs(output_path, exist_ok=True)
		note = "[OK]"
		if not os.path.exists(output_path):
			note = "[PATH MISSING]"
		elif os.access(output_file, os.W_OK):
			note = "[NOT WRITABLE]"
		else:
			valid_output_file = output_file
	return valid_output_file, note


# Look at result from scrape and produce a dictionary with relevant data or error output
def get_data_for_scrape_result(result):
	http_status_code = result.get("http_status_code", 500)
	reason = result.get("reason", "")
	print(f"SCRAPING COMPLETED {http_status_code}, {reason}")

	data = None
	error = ""
	ok = True
	if http_status_code != 200:
		error = f"http code {http_status_code} with reason {reason}"
		ok = False
	else:
		headers = result.get("headers", "")
		page_source = result.get("page_source", "")
		if not page_source:
			error = "no page_source"
			ok = False
		else:
			data = None
			try:
				data = json.loads(page_source)
			except Exception as e:
				error = f"json parse failed for {page_source[:100]} with {e}"
				ok = False
			if ok:
				t = __builtins__.type(data)
				if not data:
					error = f"json parse returned no data"
					ok = False
				# elif t is not '<class \'dict\'>':
				# 	error=f"json parse returned not dict ({t})"
				# 	ok=False
	return data, ok, error


attrs = ["millenia", "centuries", "decades", "years", "months", "days", "hours", "minutes", "seconds"]

human_readable = lambda delta: ["%d %s" % (getattr(delta, attr), getattr(delta, attr) > 1 and attr or attr[:-1]) for attr in attrs if getattr(delta, attr)]


def human_delta(td_object: datetime.timedelta, max: int = 0):
	ms = int(td_object.total_seconds() * 1000)
	if ms == 0:
		return "0 ms"
	sign = ""
	if ms < 0:
		ms = -ms
		sign = "-"
	# fmt: off
	periods = [
		("year",  1000 * 60 * 60 * 24 * 365),
		("month", 1000 * 60 * 60 * 24 * 30),
		("day",   1000 * 60 * 60 * 24),
		("hr",    1000 * 60 * 60),
		("min",   1000 * 60),
		("sec",   1000),
		("ms", 1)
	]
	# fmt: on

	strings = []
	ct: int = 0
	for period_name, period_ms in periods:
		if ms > period_ms:
			period_value, ms = divmod(ms, period_ms)
			# has_s = "s" if period_value > 1 else ""
			# strings.append("%s %s%s" % (period_value, period_name, has_s))
			strings.append(f"{period_value} {period_name}")
			ct += 1
			if max > 0 and ct > max:
				break
	return sign + ", ".join(strings)  # + f"({td_object}, {ms})"


def human_bytesize(bytes: int, max: int = 0):
	if bytes == 0:
		return "0 bytes"
	if bytes < 0:
		return "negative bytes (error)"
	# fmt: off
	KiB=1024
	periods = [
		("PiB", KiB*KiB*KiB*KiB*KiB),
		("TiB", KiB*KiB*KiB*KiB),
		("GiB", KiB*KiB*KiB),
		("MiB", KiB*KiB),
		("KiB", KiB),
		("bytes", 1)
	]
	# fmt: on

	strings = []
	ct: int = 0
	for period_name, period_bytes in periods:
		if bytes > period_bytes:
			period_value, bytes = divmod(bytes, period_bytes)
			# has_s = "s" if period_value > 1 else ""
			# strings.append("%s %s%s" % (period_value, period_name, has_s))
			strings.append(f"{period_value} {period_name}")
			ct += 1
			if max > 0 and ct > max:
				break
	return ", ".join(strings)  # + f"({td_object}, {bytes})"


# Make washee conform strictly to structure of washer
def wash_dict(washee, washer):
	out = {}
	for k, v in washer.items():
		if k in washee:
			if isinstance(v, dict):
				if isinstance(washee[k], dict):
					out[k] = wash_dict(washee[k], v)
			else:
				if not isinstance(washee[k], dict):
					out[k] = washee[k]
	return out


def random_str(l):
	return base64.b64encode(os.urandom(l))


def print_process_info():
	if hasattr(os, "getppid"):
		print(f"Parent process:{os.getppid()}")
	print(f"Process id:{os.getpid()}")


def sleep(time_sec):
	time.sleep(time_sec)
	# await asyncio.sleep async


def read_file(fname, strip=True):
	fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
	data = ""
	if os.path.exists(fn):
		with open(fn, encoding="utf-8") as f:
			data = f.read()
			data = data.strip() if strip else data
			# logger.info(f"Got data '{data}' from '{fn}'")
	else:
		logger.error(f"Could not find file {fn} relative to working directory {os.getcwd()}")
	return data


def write_file(fn, data, strip=True):
	with open(fn, "w") as f:
		f.write(data.strip() if strip else data)



def stripes(cols=79, rows=3, on=3, off=3, on_char="#", off_char=" ", offset=0, sheer=1):
	out=""
	alphabet = on_char * on + off_char * off
	alphabet_len=len(alphabet)
	for row in range(0, rows):
		index = offset
		out += termcol.ORANGE
		for col in range(0, cols):
			alphabet_index = index % alphabet_len
			out += alphabet[alphabet_index]
			index += 1
		offset+=sheer
		out += termcol.ENDC +"\n"
	return out


def debug_imports():
	import logging
	import pprint
	import sys
	import os

	l = logging.getLogger(__name__)
	l.error(f"PATH: {sys.path}")
	l.error(f"PREFIX: {sys.prefix}")
	l.error(f"ENV: {pprint.pformat(os.environ)}")

	import pkg_resources

	installed_packages = {d.project_name: d.version for d in pkg_resources.working_set}
	l.error(f"MODULES:{pprint.pformat(installed_packages)}")

	import pkgutil

	for m in pkgutil.iter_modules(path=None):
		l.error(f"MODULE: {m.name}")

	def explore_package(module_name):
		loader = pkgutil.get_loader(module_name)
		if not loader:
			l.error(f"No loader for {module_name}")
		elif not loader.filename:
			l.error(f"No filename for {module_name}")
		else:
			for sub_module in pkgutil.walk_packages([loader.filename]):
				_, sub_module_name, _ = sub_module
				qname = module_name + "." + sub_module_name
				l.error(qname)
				explore_package(qname)

	explore_package("fk")
	explore_package("batch")

	import time

	time.sleep(die_sec)
	sys.exit(6)


class TimeoutRequestsSession(requests.Session):
	def request(self, *args, **kwargs):
		kwargs.setdefault("timeout", HTTP_TIMEOUT)
		return super(TimeoutRequestsSession, self).request(*args, **kwargs)


def requests_session():
	global _requests_session_instance
	if not _requests_session_instance:
		_requests_session_instance = TimeoutRequestsSession()
		# fmt:off
		headers = {
			  "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36"
			, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
			, "Cache-Control": "no-cache"
			, "Pragma": "no-cache"
		}
		# fmt:on
		_requests_session_instance.headers.update(headers)
	return _requests_session_instance


def list_all_pkg():
	for name in sys.modules.keys():
		logger.info(f"Found package: {name}")


def walk_pkg(root: str, base_dir: str = "./", path: str = "", do_debug=False):
	if do_debug and False:
		logger.info(
			f"""walk_pkg(root={root}
, base_dir={base_dir}
, path={path})\n"""
		)
	for name in pkg_resources.resource_listdir(root, path):
		sub_path = f"{path}/{name}"
		full_path = f"{base_dir}{sub_path}"
		if pkg_resources.resource_isdir(root, full_path):
			if do_debug:
				# logger.info(f"{full_path} ------------------\n")
				pass
			walk_pkg(root, base_dir, sub_path, do_debug)
		else:
			# content = pkg_resources.resource_string(root, sub_path)
			if do_debug:
				logger.info(f"  +  {full_path}\n")
			# Do something with the file content


def get_package_file_content(base, filename, do_debug=False):
	"""Look for file relative to package root and return it's content"""
	content = ""
	package_base_path: str = os.path.abspath(os.path.join(os.path.dirname(base), "../"))
	if do_debug:
		logger.warn(f"package_base_path={package_base_path}")
		logger.warn(f"filename={filename}")
		logger.warn(f"__name__={__name__}")
		logger.warn(f"base={base}")
	ex = False
	try:
		ex = pkg_resources.resource_exists(base, filename)
	except Exception as e:
		logger.error(f"Could not find package '{base}' ({filename}). Se alternatives:")
		list_all_pkg()
	if ex:
		logger.info(f"Fetching {filename} from package")
		content = pkg_resources.resource_string(base, filename).decode("utf-8").strip()
	else:
		logger.warning(f"No content found for {filename}")
	return content


def synchronize(corutine):
	try:
		loop = asyncio.get_running_loop()
	# 'RuntimeError: There is no current event loop...'
	except RuntimeError:
		loop = None
	if loop and loop.is_running():
		tsk = loop.create_task(corutine)
	else:
		asyncio.run(corutine)


def relurl(base):
	out = ""
	if base:
		try:
			base = str(base)
			o = urlparse(base)
			out = o.path
			if o.params:
				out +=o.params
			if o.query:
				out +="?"
				out +=o.query
			if o.fragment:
				out +="#"
				out +=o.fragment
			return out
		except Exception as e:
			logger.exception(e)
			out = ""
	# logger.info(f"'{base}'({type(base)}) --> '{out}'")
	return out


def inject_env(vars):
	# Fake it by inserting values into environment
	for key, val in vars.items():
		os.environ[key] = val
	



def calculate_unique_key(dictionary):
	json_str = json.dumps(dictionary, sort_keys=True)
	unique_key = hashlib.sha256(json_str.encode()).hexdigest()
	return unique_key


def delete_file(filename, do_debug = False):
	if os.path.exists(filename):
		if do_debug:
			logger.info(f"Deleting {filename}")
		os.unlink(filename)
	else:
		if do_debug:
			logger.info(f"Already missing, not deleting {filename}")




def print_caller_info():
	# Get the current stack frame
	stack = inspect.stack()
	
	# The caller is the previous frame in the stack.
	# stack[0] is the current frame, so stack[1] is the caller.
	# You might adjust the index based on your specific needs.
	caller_frame = stack[2]
	
	# Extract information about the caller
	module = inspect.getmodule(caller_frame[0])
	module_name = module.__name__ if module else ''
	filename = caller_frame.filename
	lineno = caller_frame.lineno
	function_name = caller_frame.function
	
	# Print information about the caller
	logger.info(f'INSPECTIFY ### {module_name}::{function_name}() @ {filename}:{lineno}')

def wrap_inspect(method):
	def wrapper(*args, **kwargs):
		print_caller_info()
		return method(*args, **kwargs)
	return wrapper


# Decorate each member function with `wrap_inspect`
def inspectify(clazz):
	for attr_name in dir(clazz):
		attr = getattr(clazz, attr_name)
		if callable(attr) and not attr_name.startswith("__"):
			setattr(clazz, attr_name, wrap_inspect(attr))


def indent(raw, space="\t\t"):
	nspace = ""
	try:
		nspace = int(space)
	except:
		pass
	if space == str(nspace):
		space = " " * nspace
	return space + (space + '\n').join(raw.split('\n'))


def random_token(length=10):
	alphabet = string.ascii_letters + string.digits
	return "".join(random.choice(alphabet) for i in range(length))


def generate_tree(directory, prefix=''):
	tree_str = ""
	files = sorted(os.listdir(directory))
	for i, file in enumerate(files):
		path = os.path.join(directory, file)
		if os.path.isdir(path):
			tree_str += f"{prefix}{'├' if i < len(files) - 1 else '└'}─ {termcol.BLUE}{file}{termcol.ENDC}\n"
			extension = '│  ' if i < len(files) - 1 else '    '
			tree_str += generate_tree(path, prefix=prefix + extension)
		else:
			bytesize = human_bytesize(os.path.getsize(path), 0)
			tree_str += f"{prefix}{'├' if i < len(files) - 1 else '└'}─ {termcol.GREEN}{file}{termcol.ENDC} [{bytesize}]\n"
	return tree_str


def tree(directory):
	return f".\n{generate_tree(directory)}"


def get_package_relative_dir(do_debug = False):
	path = pathlib.Path(__file__).resolve()
	if do_debug:
		logger.info(f"get_package_relative_dir file: '{path}' is file: {path.is_file()}")
	path = path.parent
	if do_debug:
		logger.info(f"get_package_relative_dir path: '{path}' is dir: {path.is_dir()}")
	if do_debug:
		logger.info(f"\n{tree(path)}")
	return path


def get_package_root_dir(package_name = __name__, do_debug = False):
	if "__main__" == package_name:
		logger.warning("Main script detected, aborting")
		return None
	if do_debug:
		logger.info(f"          package_name:{package_name}")
	package_parts = package_name.split(".")
	part_count = len(package_parts)
	spec = importlib.util.find_spec(package_name)
	if do_debug:
		logger.info(f"                  spec:{pprint.pformat(spec)}")
	if spec and spec.origin:
		root_path = pathlib.Path(spec.origin)
		for i in range(0, part_count):
			root_path = root_path.parent
		if do_debug:
			logger.info(f"             root_path: {root_path}")
		return root_path
	logger.warning(f"Could not find package root for {package_name}, aborting")
	return None


def xray(o, max_level=10):
	class xs:
		endc = termcol.ENDC
		punctuation = termcol.WHITE
		warning = termcol.ORANGE
		error = termcol.RED
		info = termcol.BLUE
		base_type = termcol.YELLOW
		list = termcol.CYAN
		dict = termcol.MAGENTA
		key = termcol.DARK_MAGENTA
		object = termcol.GREEN
		callable = termcol.GREEN
		method = termcol.DARK_GREEN
		callable_internal = termcol.RED
		method_internal = termcol.DARK_RED
	seen = set()
	map = {
		  'list':{'(':'[', ')':']'}
		, 'set':{'(':'((', ')':'))'}
		, 'tuple':{'(':'(', ')':')'}
		, 'dict':{'(':'{', ')':'}'}
	}
	do_debug = False
	indent_template = "  "
	def _x(obj, level):
		print(pprint.pformat(obj))
		# Base indentation for nested structures
		base_indent = indent_template * level

		# Create an object identifier to track if we have seen this object before
		obj_id = id(obj)
		if False and obj_id in seen:
			ret = base_indent + xs.warning + "Cyclic reference detected." + xs.endc
			return ret, "error"
	
		if level > max_level:
			ret = base_indent + xs.warning + "Max level reached." + xs.endc
			return ret, "error"
		
		# Add the current object to the seen set
		seen.add(obj_id)
	
		# If the object is one of the basic data types, just print it directly
		if isinstance(obj, (int, float, str, bool, type(None))):
			if do_debug:
				print(f"\ndetected base {pprint.pformat(obj)}\n")
			return xs.base_type + repr(obj) + xs.endc, "base"
	
		# If the object is a list, tuple or set, iterate through its items
		if isinstance(obj, (list, tuple, set)):
			#print(f"\ndetect list {pprint.pformat(obj)}\n")
			col = list()
			t = type(obj).__name__
			p = map[t]
			l = len(obj)
			for item in obj:
				col.append(_x(item, level + 1))
			tuck = True
			if l > 10:
				tuck = False
			if tuck:
				ret = xs.list + p['('] + xs.endc
				for tup in sorted(col, key=lambda x: (x[1], x[0])):
					ret += tup[0] + xs.punctuation + ', ' + xs.endc
				ret += xs.list + p[')'] + xs.endc + "\n"
				if do_debug:
					print(f"\ndetect list {pprint.pformat(obj)} returns\n {ret}\n")
			else:
				ret = base_indent + xs.list + p['('] + xs.endc + "\n"
				for tup in sorted(col, key=lambda x: (x[1], x[0])):
					ret += tup[0] + "\n"
				ret += base_indent + xs.list + p[')'] + xs.endc + "\n"
				if do_debug:
					print(f"\ndetect list {pprint.pformat(obj)} returns\n  {ret}\n")
			return ret, "list"
	
		# If the object is a dictionary, iterate through its keys and values
		if isinstance(obj, dict):
			#print(f"\ndetect dict {pprint.pformat(obj)}\n")
			col = list()
			t = type(obj).__name__
			p = map[t]
			initial_indent = ""
			for key, value in obj.items():
				pre = base_indent + initial_indent + xs.key + repr(key) + xs.punctuation + ": " + xs.endc
				tup = _x(value, level + 2)
				col.append( (pre + tup[0], tup[1]) )
				initial_indent = indent_template
			ret = xs.dict + p['('] + xs.endc + "\n"
			for tup in sorted(col, key=lambda x: (x[1], x[0])):
				ret += tup[0] + "\n"
			ret += base_indent +  xs.dict + p[')'] + xs.endc + "\n"
			if do_debug:
				print(f"\ndetect dict {pprint.pformat(obj)} returns\n  {ret}\n")
			return ret, "dict"
		if do_debug:
			print(f"\nundetected {pprint.pformat(obj)}\n")
		ret = base_indent + type(obj).__name__ + xs.punctuation + ": " + xs.endc
		return ret, "unknown"
	
	def lol():
		# Print type of object if it's not a basic type or container
		print(base_indent + type(obj).__name__ + xs.punctuation + ": " + xs.endc)
		
		# Use dir() to get a list of attributes and methods of the object
		attrs = dir(obj)
		for attr in attrs:
			try:
				# Identify private and special methods
				is_internal = attr.startswith('__') and attr.endswith('__')
				maybe_internal_callable = xs.callable_internal if is_internal else xs.callable
				maybe_internal_method = xs.method_internal if is_internal else xs.method
				value = getattr(obj, attr)
				# If value is callable (method), we represent it but don't call it
				if callable(value):
					print(base_indent + indent_template + xs.callable + attr + xs.punctuation + "():"+ xs.info + "Method" + xs.endc )
				else:
					print(base_indent + indent_template + xs.callable + attr + xs.punctuation + ":" + xs.endc , end="" )
					_x(value, level + 1)
			except Exception as e:
				
				print(base_indent + indent_template + xs.error + attr + xs.punctuation + ":" + xs.error + str(e) + xs.endc)

	ret, t = _x(o, 0)
	return ret

