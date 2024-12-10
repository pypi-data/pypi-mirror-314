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


expected_schema = [{'default': {'type': 'number', 'value': 1},
'description': 'DIN-780 standard tooth height',
'name': 'modul',
'schema': {'raw': '[0.05, 0.06, 0.08, 0.10, 0.12, '
				  '0.16,0.20,0.25,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.25,1.5,2,2.5,3,4,5,6,8,10,12,16,20,25,32,40,50,60]',
		   'values': [0.05,
					  0.06,
					  0.08,
					  0,
					  0.12,
					  0.16,
					  0,
					  0.25,
					  0.3,
					  0.4,
					  0.5,
					  0.6,
					  0.7,
					  0.8,
					  0.9,
					  1,
					  1.25,
					  1.5,
					  2,
					  2.5,
					  3,
					  4,
					  5,
					  6,
					  8,
					  10,
					  12,
					  16,
					  20,
					  25,
					  32,
					  40,
					  50,
					  60]},
'section': 'Spur Gear'},
{'default': {'type': 'number', 'value': 20},
'description': 'Number of teeth',
'name': 'tooth_count',
'schema': {'max': 30, 'min': 2, 'raw': '[2:30]', 'step': 0},
'section': 'Spur Gear'},
{'default': {'type': 'number', 'value': 40},
'description': 'Length',
'name': 'length',
'schema': {'max': 100, 'min': 1, 'raw': '[1:100]', 'step': 0},
'section': 'Spur Gear'},
{'default': {'type': 'number', 'value': 4},
'description': 'Height',
'name': 'height',
'schema': {'max': 100, 'min': 1, 'raw': '[1:100]', 'step': 0},
'section': 'Spur Gear'},
{'default': {'type': 'number', 'value': 8},
'description': 'Width',
'name': 'width',
'schema': {'max': 100, 'min': 1, 'raw': '[1:100]', 'step': 0},
'section': 'Spur Gear'},
{'default': {'type': 'number', 'value': 2},
'description': 'Bore diameter',
'name': 'bore',
'schema': {'label': 'default',
		   'labels': {2: 'default', '0': 80},
		   'raw': '[0:80]'},
'section': 'Spur Gear'},
{'default': {'type': 'bool', 'value': True},
'description': 'Remove uneccessary material from gears',
'name': 'optimize',
'schema': {'debug': 'NO SCHEMA FOR None with type bool'},
'section': 'Spur Gear'},
{'default': {'type': 'number', 'value': 30},
'description': 'Attack angle',
'name': 'attack_angle',
'schema': {'label': 'default',
		   'labels': {30: 'default', '0': 30},
		   'raw': '[0:30]'},
'section': 'Teeth'},
{'default': {'type': 'number', 'value': 20},
'description': 'Helix angle (for helix and herringbone teeth)',
'name': 'helix_angle',
'schema': {'label': 'default',
		   'labels': {20: 'default', '0': 30},
		   'raw': '[0:30]'},
'section': 'Teeth'},
{'default': {'type': 'bool', 'value': False},
'description': 'Use herring bone teeth',
'name': 'herringbone',
'schema': {'debug': 'NO SCHEMA FOR None with type bool'},
'section': 'Teeth'},
{'default': {'type': 'bool', 'value': True},
'description': 'Include pinion gear',
'name': 'pair',
'schema': {'debug': 'NO SCHEMA FOR None with type bool'},
'section': 'Pinion Gear'},
{'default': {'type': 'bool', 'value': True},
'description': 'Show parts as assembled',
'name': 'assembled',
'schema': {'debug': 'NO SCHEMA FOR None with type bool'},
'section': 'Pinion Gear'},
{'default': {'type': 'number', 'value': 2},
'description': 'Bore diameter',
'name': 'bore_secondary',
'schema': {'label': 'default',
		   'labels': {2: 'default', '0': 80},
		   'raw': '[0:80]'},
'section': 'Pinion Gear'},
{'default': {'type': 'number', 'value': 10},
'description': 'Number of teeth',
'name': 'tooth_count_secondary',
'schema': {'max': 30, 'min': 2, 'raw': '[2:30]', 'step': 0},
'section': 'Pinion Gear'}]


def test_openscad_parse():
	logger.info("openscad parse unit test")
	local_name_openscad = os.path.join(data_dir, "customizer.scad")
	with open(local_name_openscad, "r") as f:
		source = f.read()
		schema = openscad.parse_customize(source)
		logger.info("SCHEMA:")
		logger.info(pprint.pformat(schema))
		#assert(expected_schema == schema)
		logger.info("SOURCE:")
		logger.info(source)

	
def test_openscad_render():
	logger.info("openscad render unit test")
	do_debug = True
	set_name = "set"
	local_name_openscad = os.path.join(data_dir, "Spur.scad")
	local_name_stl = f"{local_name_openscad}.stl"
	local_name_png = f"{local_name_openscad}.png"
	local_name_json = f"{local_name_openscad}.json"
	#json_parameters = json.dumps(openscad_parameters, indent=3, sort_keys=True)
	logger.info(f"do_debug:{do_debug}")
	logger.info(f"set_name:{set_name}")
	logger.info(f"local_name_openscad:{local_name_openscad}")
	logger.info(f"local_name_stl:{local_name_stl}")
	logger.info(f"local_name_json:{local_name_json}")
	stl_scad = openscad.OpenScadRunner(
		scriptfile = local_name_openscad
		, outfiles = [local_name_stl, local_name_png]
		, customizer_file = local_name_json
		, customizer_sets = [set_name]
		, auto_center = True
		, view_all = True
		, verbose = do_debug or True)
	ok, err = stl_scad.run()
	logger.info(f"success:{stl_scad.success}")
	logger.info(f"return_code:{stl_scad.return_code}")
	logger.info(f"OK:{ok}")
	logger.info(f"err:{err}")
	return True




test_cases = [
	{
		"markup": """
/* [Drop down box] */
// combo box for number
Numbers=2; // [0, 1, 2, 3]
	""",
		"expected": None,
	},
	{
		"markup": """
/* [Drop down box] */
// combo box for string
Strings="foo"; // [foo, bar, baz]
""",
		"expected": [{'default': {'type': 'string', 'value': 'foo'},
		'description': 'combo box for string',
		'name': 'Strings',
		'schema': {'raw': '[foo, bar, baz]', 'values': ['foo', 'bar', 'baz']},
		'section': 'Drop down box'
		}],
	},
	{
		"markup": """
/* [Drop down box] */
// labeled combo box for numbers
Labeled_values=10; // [10:L, 20:M, 30:XL]
""",
		"expected": [{'default': {'type': 'number', 'value': '10'},
		'description': 'labeled combo box for numbers',
		'name': 'Labeled_values',
		'schema': {'labels': {10: 'L', 20: 'M', 30: 'XL'},
				   'raw': '[10:L, 20:M, 30:XL]'},
		'section': 'Drop down box',
		}],
	},
	{
		"markup": """
/* [Drop down box] */
// labeled combo box for string
Labeled_value="S"; // [S:Small, M:Medium, L:Large]
""",
		"expected": 
			  [{'default': {'type': 'string', 'value': 'S'}
			, 'description': 'labeled combo box for string'
			, 'name': 'Labeled_value'
			, 'schema': {'labels': {'L': 'Large', 'M': 'Medium', 'S': 'Small'},
						 'raw': '[S:Small, M:Medium, L:Large]'},
			  'section': 'Drop down box'}]
	},
	{
		"markup": """
/*[ Slider ]*/
// slider widget for number
slider =34; // [10:100]
""",
		"expected": None,
	},
	{
		"markup": """
/*[ Slider ]*/
// step slider for number
stepSlider=2; //[0:5:100]
""",
		"expected": None,
	},
	{
		"markup": """
/* [Checkbox] */
// description
Variable = true;
""",
		"expected": None,
	},
	{
		"markup": """
/* [Spinbox] */
// spinbox with step size 1
Spinbox1 = 5;
""",
		"expected": None,
	},
	{
		"markup": """
/* [Spinbox with unit] */
// spinbox with step size 1 and unit
Spinbox2 = 5; // (mm)
		""",
		"expected": None,
	},
	{
		"markup": """
/* [Textbox] */
// Text box for vector with more than 4 elements
Vector6=[12,34,44,43,23,23];
""",
		"expected": None,
	},
	{
		"markup": """
/* [Textbox] */
// Text box for string
String="hello";
""",
		"expected": None,
	},
	{
		"markup": """
/* [Vector] */
// Text box for vector with 1 element
Vector1=[12]; //[0:2:50]
""",
		"expected": None,
	},
	{
		"markup": """
/* [Vector] */
// Text box for vector with 2 elements
Vector2=[12,34]; //[0:2:50]
""",
		"expected": None,
	},
	{
		"markup": """
/* [Vector] */
// Text box for vector with 3 elements
Vector3=[12,34,46]; //[0:2:50]
""",
		"expected": None,
	},
	{
		"markup": """
/* [Vector] */
// Text box for vector with 4 elements
Vector4=[12,34,46,24]; //[0:2:50]
""",
		"expected": None,
	},
]


def lol_test_openscad_parse_cases():
	for test_case in test_cases:
		source = test_case.get("markup")
		expected_schema = test_case.get("expected")
		schema = openscad.parse_customize(source, do_debug = False)
		if expected_schema:
			logger.info("-----------------------------------------------------\n"+source+"\n")
			logger.info("SCHEMA:\n\n"+pprint.pformat(schema)+"\n")
			logger.info("EXPECTED:\n\n"+pprint.pformat(expected_schema)+"\n")
			assert(expected_schema == schema)


regexes = {
"decimal_number_re":{
		"regex": re.compile(openscad.decimal_number_inc)
		, "tests":{
			  ".0": {}
			  , "": None
			  , "X": None
			, "0.0": {}
			, "-0.0": {}
		}
	}
	, "quoted_string_re":{
		"regex": re.compile(openscad.quoted_string_inc)
		, "tests":{
			  "'bob'": {'value': 'bob'}
			, "\"lol\"": {'value': 'lol'}
			, "''": {'value': ''}
			, "\"\"": {'value': ''}
			, "'\"": None
			, "'123345456567679780qwertyuiopåæasdfghjkløæzxcvbnm,.!\"#¤#¤%&%&/&/()/()=()=?'":  {'value': '123345456567679780qwertyuiopåæasdfghjkløæzxcvbnm,.!"#¤#¤%&%&/&/()/()=()=?'}
		}
	}
	, "unit_re":{
		"regex": re.compile(openscad.unit_inc)
		, "tests":{
			  "(mm)": {'unit': 'mm'}
			, "()": None
		}
	}
	, "h1_re":{
		"regex": openscad.h1_re
		, "tests":{
			  "/* [Section name] */": {'section': 'Section name'}
			, "/* [Section name] */": {'section': 'Section name'}
			, "/* [ Section name] */": {'section': 'Section name'}
			, "/* [Section name ] */": {'section': 'Section name'}
			, "/* [ Section name ] */": {'section': 'Section name'}
			, "/* [Section name]  */": {'section': 'Section name'}
			, "/*  [Section name] */": {'section': 'Section name'}
			, "/*[Section name] */": {'section': 'Section name'}
			, "/* [Section name]*/": {'section': 'Section name'}
			, "/*[Section name]*/": {'section': 'Section name'}
			, "/*[e]*/": {'section': 'e'}
			, "/* [ e ] */": {'section': 'e'}
			, "/*[]*/": None
			, "/* [ ] */": None
			, "/* [ e ] * /": None
			, "/* [ ] * /": None
			, "": None
		}
	}
	, "h2_re":{
		"regex": openscad.h2_re
		, "tests":{
			  "// Variable description": {'description': 'Variable description', 'unit': None}
			, " // Variable description": {'description': 'Variable description', 'unit': None}
			, "// Variable description": {'description': 'Variable description', 'unit': None}
			, "//  Variable description": {'description': 'Variable description', 'unit': None}
			, "/ / Variable description": None
			, "/ /Variable description": None
			, "// Variable description ": {'description': 'Variable description', 'unit': None}
			, "// Variabledescription": {'description': 'Variabledescription', 'unit': None}
			, " // Variable description ": {'description': 'Variable description', 'unit': None}
			, " // Variabledescription": {'description': 'Variabledescription', 'unit': None}
			, "/ / Variable description ": None
			, "/ / Variabledescription": None
			, " / / Variable description ": None
			, " / / Variabledescription": None
			, "//": None
		}
	}
	, "var_re":{
		"regex": openscad.var_re
		, "tests":{
			  ".0": None
			, "Variable = definition": None
			, "Variable = definition;": {'variable': 'Variable', 'value': 'definition', 'comment': None}
			, "lolbob = badabing; // comment": {'comment': 'comment', 'value': 'badabing', 'variable': 'lolbob'}
			, "  lolbob   =   badabing  ; //    comment": {'comment': 'comment', 'value': 'badabing', 'variable': 'lolbob'}
			, "lolbob=badabing;//comment": {'comment': 'comment', 'value': 'badabing', 'variable': 'lolbob'}
			, "  lolbob   =   badabing  ; / /    comment": None
			, "lolbob = badabing;": {'comment': None, 'value': 'badabing', 'variable': 'lolbob'}
			, "  lolbob = badabing;": {'comment': None, 'value': 'badabing', 'variable': 'lolbob'}
			, "  lolbob   = badabing  ;   ": {'comment': None, 'value': 'badabing', 'variable': 'lolbob'}
			, "lolbob=badabing;": {'comment': None, 'value': 'badabing', 'variable': 'lolbob'}
			, "lolbob = badabing //": None
			, "lolbob = badabing": None
			, "lolbob = badabing  ": None
			, "  lolbob = badabing": None
			, "lolbob=badabing": None
			, "lolbob = badabing;": {'comment': None, 'value': 'badabing', 'variable': 'lolbob'}
			, "X": None
			, "0.0": None
			, "-0.0": None
		}
	}
	, "bool_val_re":{
		"regex": openscad.bool_val_re
		, "tests":{
			  ".0": None
			, "": None
			, " false ": {'value': 'false'}
			, " false": {'value': 'false'}
			, " true ": {'value': 'true'}
			, " true": {'value': 'true'}
			, "false ": {'value': 'false'}
			, "false": {'value': 'false'}
			, "true ": {'value': 'true'}
			, "true": {'value': 'true'}
			, "X": None
			, "0.0": None
			, "-0.0": None
		}
	}
	, "string_val_re":{
		"regex": openscad.string_val_re
		, "tests":{
			  ".0": None
			, "": None
			, "X": None
			, "0.0": None
			, "-0.0": None
			, "''": None
			, "\"\"": None
			, "X": None
			, "0.0": None
			, "-0.0": None
			, "'bob'": {'value': 'bob'}
			, "\"lol\"": {'value': 'lol'}
			, "''": {'value': ''}
			, "\"\"": {'value': ''}
			, "'\"": None
			, "'123345456567679780qwertyuiopåæasdfghjkløæzxcvbnm,.!\"#¤#¤%&%&/&/()/()=()=?'":  {'value': '123345456567679780qwertyuiopåæasdfghjkløæzxcvbnm,.!"#¤#¤%&%&/&/()/()=()=?'}
			, " 'bob'": {'value': 'bob'}
			, " \"lol\"": {'value': 'lol'}
			, " ''": {'value': ''}
			, " \"\"": {'value': ''}
			, " '\"": None
			, " '123345456567679780qwertyuiopåæasdfghjkløæzxcvbnm,.!\"#¤#¤%&%&/&/()/()=()=?'":  {'value': '123345456567679780qwertyuiopåæasdfghjkløæzxcvbnm,.!"#¤#¤%&%&/&/()/()=()=?'}
			, "'bob' ": {'value': 'bob'}
			, "\"lol\" ": {'value': 'lol'}
			, "'' ": {'value': ''}
			, "\"\" ": {'value': ''}
			, "'\" ": None
			, "'123345456567679780qwertyuiopåæasdfghjkløæzxcvbnm,.!\"#¤#¤%&%&/&/()/()=()=?' ":  {'value': '123345456567679780qwertyuiopåæasdfghjkløæzxcvbnm,.!"#¤#¤%&%&/&/()/()=()=?'}
			, " 'bob' ": {'value': 'bob'}
			, " \"lol\" ": {'value': 'lol'}
			, " '' ": {'value': ''}
			, " \"\" ": {'value': ''}
			, " '\" ": None
			, " '123345456567679780qwertyuiopåæasdfghjkløæzxcvbnm,.!\"#¤#¤%&%&/&/()/()=()=?' ":  {'value': '123345456567679780qwertyuiopåæasdfghjkløæzxcvbnm,.!"#¤#¤%&%&/&/()/()=()=?'}
		}
	}
	, "number_val_re":{
		"regex": openscad.number_val_re
		, "tests":{
			  ".0": {'value': '.0'}
			, "": None
			, "X": None
			, "0.0": {'value': '0.0'}
			, "-0.0": {'value': '-0.0'}
		}
	}
	, "labeled_bool_schema_re":{
		"regex": openscad.labeled_bool_schema_re
		, "tests":{
			  ".0": None
			, "-0.0": None
			, " [ true:label1, false:label2 ] ": {'values': 'true:label1, false:label2'}
			, "word": None
			, "number": None
			, "true": None
			, "false": None
			, "[]": None
			, "[ ]": None
			, "[word]": None
			, "[false]": None
			, "[true]": None
			, "[false:]": None
			, "[true:]": None
			, "[false :]": None
			, "[true :]": None
			, "[ false]": None
			, "[ true]": None
			, "[ false:]": None
			, "[ true:]": None
			, "[ false :]": None
			, "[ true :]": None
			, "[false ]": None
			, "[true ]": None
			, "[false: ]": None
			, "[true: ]": None
			, "[false : ]": None
			, "[true : ]": None
			, "[ false ]": None
			, "[ true ]": None
			, "[ false: ]": None
			, "[ true: ]": None
			, "[ false : ]": None
			, "[ true : ]": None
			, "[ true:label1, false:label2, false:label2, false:label2, false:label2]": {'values': 'true:label1, false:label2, false:label2, false:label2, false:label2'}
			, "[false:label2]": {'values': 'false:label2'}
			, "[true:label2]": {'values': 'true:label2'}
			, "[ false:label2]": {'values': 'false:label2'}
			, "[ true:label2]": {'values': 'true:label2'}
			, "[false:label2 ]": {'values': 'false:label2'}
			, "[true:label2 ]": {'values': 'true:label2'}
			, "[ false:label2 ]": {'values': 'false:label2'}
			, "[ true:label2 ]": {'values': 'true:label2'}
			, "[ false:label2,false:label2]": {'values': 'false:label2,false:label2'}
			, "[ true:label2,false:label2]": {'values': 'true:label2,false:label2'}
			, "[false:label2,false:label2 ]": {'values': 'false:label2,false:label2'}
			, "[true:label2,false:label2 ]": {'values': 'true:label2,false:label2'}
			, "[ false:label2,false:label2 ]": {'values': 'false:label2,false:label2'}
			, "[ true:label2,false:label2 ]": {'values': 'true:label2,false:label2'}
			, "[ false:label2, false:label2]": {'values': 'false:label2, false:label2'}
			, "[ true:label2, false:label2]": {'values': 'true:label2, false:label2'}
			, "[false:label2, false:label2 ]": {'values': 'false:label2, false:label2'}
			, "[true:label2, false:label2 ]": {'values': 'true:label2, false:label2'}
			, "[ false:label2, false:label2 ]": {'values': 'false:label2, false:label2'}
			, "[ true:label2, false:label2 ]": {'values': 'true:label2, false:label2'}
			, "[ false:label2 ,false:label2]": {'values': 'false:label2 ,false:label2'}
			, "[ true:label2 ,false:label2]": {'values': 'true:label2 ,false:label2'}
			, "[false:label2 ,false:label2 ]": {'values': 'false:label2 ,false:label2'}
			, "[true:label2 ,false:label2 ]": {'values': 'true:label2 ,false:label2'}
			, "[ false:label2 ,false:label2 ]": {'values': 'false:label2 ,false:label2'}
			, "[ true:label2 ,false:label2 ]": {'values': 'true:label2 ,false:label2'}
			, "[ false:label2 , false:label2]": {'values': 'false:label2 , false:label2'}
			, "[ true:label2 , false:label2]": {'values': 'true:label2 , false:label2'}
			, "[false:label2 , false:label2 ]": {'values': 'false:label2 , false:label2'}
			, "[true:label2 , false:label2 ]": {'values': 'true:label2 , false:label2'}
			, "[ false:label2 , false:label2 ]": {'values': 'false:label2 , false:label2'}
			, "[ true:label2 , false:label2 ]": {'values': 'true:label2 , false:label2'}
		}
	} 
	, "values_string_schema_re":{
		"regex": openscad.values_string_schema_re
		, "tests":{
			  "": None
			, " ": None
			, "[]": None
			, " [ ] ": None
			, " [] ": None
			, "[] ": None
			, " []": None
			, "[]": None
			, "[ value1, value2, value3 ]": {'values': 'value1, value2, value3'}
			, "[value1,value2,value3]": {'values': 'value1,value2,value3'}
			, "[value1, value2, value3 ]": {'values': 'value1, value2, value3'}
			, "[ value1 , value2 , value3 ]": {'values': 'value1 , value2 , value3'}
			, "[value1:, value2, value3 ]": None
			, "[ value1: , value2 , value3 ]": None
		}
	}
	, "labeled_string_schema_re":{
		"regex": openscad.labeled_string_schema_re
		, "tests":{
			  "": None
			, " ": None
			, "[]": None
			, " [ ] ": None
			, " [] ": None
			, "[] ": None
			, " []": None
			, "[]": None
			, "[ value1, value2, value3 ]": None
			, "[value1,value2,value3]": None
			, "[value1, value2, value3 ]": None
			, "[ value1 , value2 , value3 ]": None
			, "[value1:, value2, value3 ]": None
			, "[ value1: , value2 , value3 ]": None
			, "[value1 :label1,value2: label2,value3:label3]": {'values': 'value1 :label1,value2: label2,value3:label3'}
			, "[value1 :label1, value2: label2, value3:label3]": {'values': 'value1 :label1, value2: label2, value3:label3'}
			, "[value1 :label1 ,value2: label2 ,value3:label3]": {'values': 'value1 :label1 ,value2: label2 ,value3:label3'}
			, "[value1 :label1 , value2: label2 , value3:label3]": {'values': 'value1 :label1 , value2: label2 , value3:label3'}
			, "[ value1 :label1,value2: label2,value3:label3]": {'values': 'value1 :label1,value2: label2,value3:label3'}
			, "[ value1 :label1 ,value2: label2 ,value3:label3]": {'values': 'value1 :label1 ,value2: label2 ,value3:label3'}
			, "[ value1 :label1, value2: label2, value3:label3]": {'values': 'value1 :label1, value2: label2, value3:label3'}
			, "[ value1 :label1 , value2: label2 , value3:label3]": {'values': 'value1 :label1 , value2: label2 , value3:label3'}
			, "[value1 :label1,value2: label2,value3:label3 ]": {'values': 'value1 :label1,value2: label2,value3:label3'}
			, "[value1 :label1, value2: label2, value3:label3 ]": {'values': 'value1 :label1, value2: label2, value3:label3'}
			, "[value1 :label1 ,value2: label2 ,value3:label3 ]": {'values': 'value1 :label1 ,value2: label2 ,value3:label3'}
			, "[value1 :label1 , value2: label2 , value3:label3 ]": {'values': 'value1 :label1 , value2: label2 , value3:label3'}
			, "[ value1 :label1,value2: label2,value3:label3 ]": {'values': 'value1 :label1,value2: label2,value3:label3'}
			, "[ value1 :label1, value2: label2, value3:label3 ]": {'values': 'value1 :label1, value2: label2, value3:label3'}
			, "[ value1 :label1 ,value2: label2 ,value3:label3 ]": {'values': 'value1 :label1 ,value2: label2 ,value3:label3'}
			, "[ value1 :label1 , value2: label2 , value3:label3 ]": {'values': 'value1 :label1 , value2: label2 , value3:label3'}
		}
	}
	, "range1_schema_re":{
		"regex": openscad.range1_schema_re
		, "tests":{
			  "": None
			, " ": None
			, "[]": None
			, " [ ] ": None
			, " [] ": None
			, "[] ": None
			, " []": None
			, "[]": None
			, "[0]": {'max': '0', 'unit': None}
			, "[-0]": {'max': '-0', 'unit': None}
			, "[1]": {'max': '1', 'unit': None}
			, "[-1]": {'max': '-1', 'unit': None}
			, "[.0]": {'max': '.0', 'unit': None}
			, "[-.0]": {'max': '-.0', 'unit': None}
			, "[-0.0]": {'max': '-0.0', 'unit': None}
			, "[-1.0]": {'max': '-1.0', 'unit': None}
			, "[12345.67890]": {'max': '12345.67890', 'unit': None}
			, "[-12345.67890]": {'max': '-12345.67890', 'unit': None}
			, "[0 ]": {'max': '0', 'unit': None}
			, "[-0 ]": {'max': '-0', 'unit': None}
			, "[1 ]": {'max': '1', 'unit': None}
			, "[-1 ]": {'max': '-1', 'unit': None}
			, "[.0 ]": {'max': '.0', 'unit': None}
			, "[-.0 ]": {'max': '-.0', 'unit': None}
			, "[-0.0 ]": {'max': '-0.0', 'unit': None}
			, "[-1.0 ]": {'max': '-1.0', 'unit': None}
			, "[12345.67890 ]": {'max': '12345.67890', 'unit': None}
			, "[-12345.67890 ]": {'max': '-12345.67890', 'unit': None}
			, "[ 0]": {'max': '0', 'unit': None}
			, "[ -0]": {'max': '-0', 'unit': None}
			, "[ 1]": {'max': '1', 'unit': None}
			, "[ -1]": {'max': '-1', 'unit': None}
			, "[ .0]": {'max': '.0', 'unit': None}
			, "[ -.0]": {'max': '-.0', 'unit': None}
			, "[ -0.0]": {'max': '-0.0', 'unit': None}
			, "[ -1.0]": {'max': '-1.0', 'unit': None}
			, "[ 12345.67890]": {'max': '12345.67890', 'unit': None}
			, "[ -12345.67890]": {'max': '-12345.67890', 'unit': None}
			, "[ 0 ]": {'max': '0', 'unit': None}
			, "[ -0 ]": {'max': '-0', 'unit': None}
			, "[ 1 ]": {'max': '1', 'unit': None}
			, "[ -1 ]": {'max': '-1', 'unit': None}
			, "[ .0 ]": {'max': '.0', 'unit': None}
			, "[ -.0 ]": {'max': '-.0', 'unit': None}
			, "[ -0.0 ]": {'max': '-0.0', 'unit': None}
			, "[ -1.0 ]": {'max': '-1.0', 'unit': None}
			, "[ 12345.67890 ]": {'max': '12345.67890', 'unit': None}
			, "[ -12345.67890 ]": {'max': '-12345.67890', 'unit': None}
			, "[ 1 ]()": {'max': '1', 'unit': None}
			, "[ 1 ] ()": {'max': '1', 'unit': None}
			, "[ 1 ]( )": {'max': '1', 'unit': None}
			, "[ 1 ]() ": {'max': '1', 'unit': None}
			, "[ 1 ] ( ) ": {'max': '1', 'unit': None}
			, "[ 1 ](mm)": {'max': '1', 'unit': 'mm'}
			, "[ 1 ]( mm)": {'max': '1', 'unit': 'mm'}
			, "[ 1 ]( mm )": {'max': '1', 'unit': 'mm'}
			, "[ 1 ](mm )": {'max': '1', 'unit': 'mm'}
			, "[ 1 ] ( mm )": {'max': '1', 'unit': 'mm'}
			, "[ 1 ] (mm )": {'max': '1', 'unit': 'mm'}
			, "[ 1 ] ( mm)": {'max': '1', 'unit': 'mm'}
			, "[ 1 ] (mm)": {'max': '1', 'unit': 'mm'}
			, "[ 1 ](mm) ": {'max': '1', 'unit': 'mm'}
			, "[ 1 ]( mm) ": {'max': '1', 'unit': 'mm'}
			, "[ 1 ]( mm ) ": {'max': '1', 'unit': 'mm'}
			, "[ 1 ](mm ) ": {'max': '1', 'unit': 'mm'}
			, "[ 1 ] ( mm ) ": {'max': '1', 'unit': 'mm'}
			, "[ 1 ] (mm ) ": {'max': '1', 'unit': 'mm'}
			, "[ 1 ] ( mm) ": {'max': '1', 'unit': 'mm'}
			, "[ 1 ] (mm) ": {'max': '1', 'unit': 'mm'}

		}
	}
	, "range2_schema_re":{
		"regex": openscad.range2_schema_re
		, "tests":{
			  "": None
			, " ": None
			, "[]": None
			, " [ ] ": None
			, " [] ": None
			, "[] ": None
			, " []": None
			, "[]": None
			, "[0]": None
			, "[-0]": None
			, "[1]": None
			, "[-1]": None
			, "[.0]": None
			, "[-.0]": None
			, "[-0.0]": None
			, "[-1.0]": None
			, "[12345.67890]": None
			, "[-12345.67890]": None
			, "[ 1 ](mm)": None
			, "[ 1 ]( mm)": None
			, "[ 1 ]( mm )": None
			, "[ 1 ](mm )": None
			, "[ 1 ] ( mm )": None
			, "[ 1 ] (mm )": None
			, "[ 1 ] ( mm)": None
			, "[ 1 ] (mm)": None
			, "[ 1 ](mm) ": None
			, "[ 1 ]( mm) ": None
			, "[ 1 ]( mm ) ": None
			, "[ 1 ](mm ) ": None
			, "[ 1 ] ( mm ) ": None
			, "[ 1 ] (mm ) ": None
			, "[ 1 ] ( mm) ": None
			, "[ 1 ] (mm) ": None
			, "[0:0]": {'min': '0', 'max': '0', 'unit': None}
			, "[-0:0]": {'min': '-0', 'max': '0', 'unit': None}
			, "[1:0]": {'min': '1', 'max': '0', 'unit': None}
			, "[-1:0]": {'min': '-1', 'max': '0', 'unit': None}
			, "[.0:0]": {'min': '.0', 'max': '0', 'unit': None}
			, "[-.0:0]": {'min': '-.0', 'max': '0', 'unit': None}
			, "[-0.0:0]": {'min': '-0.0', 'max': '0', 'unit': None}
			, "[-1.0:0]": {'min': '-1.0', 'max': '0', 'unit': None}
			, "[12345.67890:0]": {'min': '12345.67890', 'max': '0', 'unit': None}
			, "[-12345.67890:0]": {'min': '-12345.67890', 'max': '0', 'unit': None}
			, "[ 1:0 ](mm)": {'min': '1', 'max': '0', 'unit': 'mm'}
			, "[ 1:0 ]( mm)": {'min': '1', 'max': '0', 'unit': 'mm'}
			, "[ 1:0 ]( mm )": {'min': '1', 'max': '0', 'unit': 'mm'}
			, "[ 1:0 ](mm )": {'min': '1', 'max': '0', 'unit': 'mm'}
			, "[ 1:0 ] ( mm )": {'min': '1', 'max': '0', 'unit': 'mm'}
			, "[ 1:0 ] (mm )": {'min': '1', 'max': '0', 'unit': 'mm'}
			, "[ 1:0 ] ( mm)": {'min': '1', 'max': '0', 'unit': 'mm'}
			, "[ 1:0 ] (mm)": {'min': '1', 'max': '0', 'unit': 'mm'}
			, "[ 1:0 ](mm) ": {'min': '1', 'max': '0', 'unit': 'mm'}
			, "[ 1:0 ]( mm) ": {'min': '1', 'max': '0', 'unit': 'mm'}
			, "[ 1:0 ]( mm ) ": {'min': '1', 'max': '0', 'unit': 'mm'}
			, "[ 1:0 ](mm ) ": {'min': '1', 'max': '0', 'unit': 'mm'}
			, "[ 1:0 ] ( mm ) ": {'min': '1', 'max': '0', 'unit': 'mm'}
			, "[ 1:0 ] (mm ) ": {'min': '1', 'max': '0', 'unit': 'mm'}
			, "[ 1:0 ] ( mm) ": {'min': '1', 'max': '0', 'unit': 'mm'}
			, "[ 1:0 ] (mm) ": {'min': '1', 'max': '0', 'unit': 'mm'}
		}
	}
	, "range3_schema_re":{
		"regex": openscad.range3_schema_re
		, "tests":{
			  "": None
			, " ": None
			, "[]": None
			, " [ ] ": None
			, " [] ": None
			, "[] ": None
			, " []": None
			, "[]": None
			, "[0]": None
			, "[-0]": None
			, "[1]": None
			, "[-1]": None
			, "[.0]": None
			, "[-.0]": None
			, "[-0.0]": None
			, "[-1.0]": None
			, "[12345.67890]": None
			, "[-12345.67890]": None
			, "[ 1 ](mm)": None
			, "[ 1 ]( mm)": None
			, "[ 1 ]( mm )": None
			, "[ 1 ](mm )": None
			, "[ 1 ] ( mm )": None
			, "[ 1 ] (mm )": None
			, "[ 1 ] ( mm)": None
			, "[ 1 ] (mm)": None
			, "[ 1 ](mm) ": None
			, "[ 1 ]( mm) ": None
			, "[ 1 ]( mm ) ": None
			, "[ 1 ](mm ) ": None
			, "[ 1 ] ( mm ) ": None
			, "[ 1 ] (mm ) ": None
			, "[ 1 ] ( mm) ": None
			, "[ 1 ] (mm) ": None
			, "[0:0]": None
			, "[-0:0]": None
			, "[1:0]": None
			, "[-1:0]": None
			, "[.0:0]": None
			, "[-.0:0]": None
			, "[-0.0:0]": None
			, "[-1.0:0]": None
			, "[12345.67890:0]": None
			, "[-12345.67890:0]": None
			, "[ 1:0 ](mm)": None
			, "[ 1:0 ]( mm)": None
			, "[ 1:0 ]( mm )": None
			, "[ 1:0 ](mm )": None
			, "[ 1:0 ] ( mm )": None
			, "[ 1:0 ] (mm )": None
			, "[ 1:0 ] ( mm)": None
			, "[ 1:0 ] (mm)": None
			, "[ 1:0 ](mm) ": None
			, "[ 1:0 ]( mm) ": None
			, "[ 1:0 ]( mm ) ": None
			, "[ 1:0 ](mm ) ": None
			, "[ 1:0 ] ( mm ) ": None
			, "[ 1:0 ] (mm ) ": None
			, "[ 1:0 ] ( mm) ": None
			, "[ 1:0 ] (mm) ": None
			, "[0:0:0]": {'min': '0', 'step': '0', 'max': '0', 'unit': None}
			, "[-0:0:0]": {'min': '-0', 'step': '0', 'max': '0', 'unit': None}
			, "[1:0:0]": {'min': '1', 'step': '0', 'max': '0', 'unit': None}
			, "[-1:0:0]": {'min': '-1', 'step': '0', 'max': '0', 'unit': None}
			, "[.0:0:0]": {'min': '.0', 'step': '0', 'max': '0', 'unit': None}
			, "[-.0:0:0]": {'min': '-.0', 'step': '0', 'max': '0', 'unit': None}
			, "[-0.0:0:0]": {'min': '-0.0', 'step': '0', 'max': '0', 'unit': None}
			, "[-1.0:0:0]": {'min': '-1.0', 'step': '0', 'max': '0', 'unit': None}
			, "[12345.67890:0:0]": {'min': '12345.67890', 'step': '0', 'max': '0', 'unit': None}
			, "[-12345.67890:0:0]": {'min': '-12345.67890', 'step': '0', 'max': '0', 'unit': None}
			, "[ 1:0:0 ](mm)": {'min': '1', 'step': '0', 'max': '0', 'unit': 'mm'}
			, "[ 1:0:0 ]( mm)": {'min': '1', 'step': '0', 'max': '0', 'unit': 'mm'}
			, "[ 1:0:0 ]( mm )": {'min': '1', 'step': '0', 'max': '0', 'unit': 'mm'}
			, "[ 1:0:0 ](mm )": {'min': '1', 'step': '0', 'max': '0', 'unit': 'mm'}
			, "[ 1:0:0 ] ( mm )": {'min': '1', 'step': '0', 'max': '0', 'unit': 'mm'}
			, "[ 1:0:0 ] (mm )": {'min': '1', 'step': '0', 'max': '0', 'unit': 'mm'}
			, "[ 1:0:0 ] ( mm)": {'min': '1', 'step': '0', 'max': '0', 'unit': 'mm'}
			, "[ 1:0:0 ] (mm)": {'min': '1', 'step': '0', 'max': '0', 'unit': 'mm'}
			, "[ 1:0:0 ](mm) ": {'min': '1', 'step': '0', 'max': '0', 'unit': 'mm'}
			, "[ 1:0:0 ]( mm) ": {'min': '1', 'step': '0', 'max': '0', 'unit': 'mm'}
			, "[ 1:0:0 ]( mm ) ": {'min': '1', 'step': '0', 'max': '0', 'unit': 'mm'}
			, "[ 1:0:0 ](mm ) ": {'min': '1', 'step': '0', 'max': '0', 'unit': 'mm'}
			, "[ 1:0:0 ] ( mm ) ": {'min': '1', 'step': '0', 'max': '0', 'unit': 'mm'}
			, "[ 1:0:0 ] (mm ) ": {'min': '1', 'step': '0', 'max': '0', 'unit': 'mm'}
			, "[ 1:0:0 ] ( mm) ": {'min': '1', 'step': '0', 'max': '0', 'unit': 'mm'}
			, "[ 1:0:0 ] (mm) ": {'min': '1', 'step': '0', 'max': '0', 'unit': 'mm'}
		}
	}
	, "labeled_number_schema_re":{
		"regex": openscad.labeled_number_schema_re
		, "tests":{
			  "": None
			, " ": None
			, "[]": None
			, " [ ] ": None
			, " [] ": None
			, "[] ": None
			, " []": None
			, "[]": None
			, "[ value1, value2, value3 ]": None
			, "[value1,value2,value3]": None
			, "[value1, value2, value3 ]": None
			, "[ value1 , value2 , value3 ]": None
			, "[value1:, value2, value3 ]": None
			, "[ value1: , value2 , value3 ]": None
			, "[ 1, 2, 3 ]": None
			, "[1,2,3]": None
			, "[1, 2, 3 ]": None
			, "[ 1 , 2 , 3 ]": None
			, "[1:, 2, 3 ]": None
			, "[ 1: , 2 , 3 ]": None

			, "[value1 :label1,value2: label2,value3:label3]": None
			, "[value1 :label1, value2: label2, value3:label3]": None
			, "[value1 :label1 ,value2: label2 ,value3:label3]": None
			, "[value1 :label1 , value2: label2 , value3:label3]": None
			, "[ value1 :label1,value2: label2,value3:label3]": None
			, "[ value1 :label1 ,value2: label2 ,value3:label3]": None
			, "[ value1 :label1, value2: label2, value3:label3]": None
			, "[ value1 :label1 , value2: label2 , value3:label3]": None
			, "[value1 :label1,value2: label2,value3:label3 ]": None
			, "[value1 :label1, value2: label2, value3:label3 ]": None
			, "[value1 :label1 ,value2: label2 ,value3:label3 ]": None
			, "[value1 :label1 , value2: label2 , value3:label3 ]": None
			, "[ value1 :label1,value2: label2,value3:label3 ]": None
			, "[ value1 :label1, value2: label2, value3:label3 ]": None
			, "[ value1 :label1 ,value2: label2 ,value3:label3 ]": None
			, "[ value1 :label1 , value2: label2 , value3:label3 ]": None
			
			
			, "[1 :label1,2: label2,3:label3]": {'values': '1 :label1,2: label2,3:label3', 'unit': None}
			, "[1 :label1, 2: label2, 3:label3]": {'values': '1 :label1, 2: label2, 3:label3', 'unit': None}
			, "[1 :label1 ,2: label2 ,3:label3]": {'values': '1 :label1 ,2: label2 ,3:label3', 'unit': None}
			, "[1 :label1 , 2: label2 , 3:label3]": {'values': '1 :label1 , 2: label2 , 3:label3', 'unit': None}
			, "[ 1 :label1,2: label2,3:label3]": {'values': '1 :label1,2: label2,3:label3', 'unit': None}
			, "[ 1 :label1 ,2: label2 ,3:label3]": {'values': '1 :label1 ,2: label2 ,3:label3', 'unit': None}
			, "[ 1 :label1, 2: label2, 3:label3]": {'values': '1 :label1, 2: label2, 3:label3', 'unit': None}
			, "[ 1 :label1 , 2: label2 , 3:label3]": {'values': '1 :label1 , 2: label2 , 3:label3', 'unit': None}
			, "[1 :label1,2: label2,3:label3 ]": {'values': '1 :label1,2: label2,3:label3', 'unit': None}
			, "[1 :label1 ,2: label2 ,3:label3 ]": {'values': '1 :label1 ,2: label2 ,3:label3', 'unit': None}
			, "[1 :label1, 2: label2, 3:label3 ]": {'values': '1 :label1, 2: label2, 3:label3', 'unit': None}
			, "[1 :label1 , 2: label2 , 3:label3 ]": {'values': '1 :label1 , 2: label2 , 3:label3', 'unit': None}
			, "[ 1 :label1,2: label2,3:label3 ]": {'values': '1 :label1,2: label2,3:label3', 'unit': None}
			, "[ 1 :label1, 2: label2, 3:label3 ]": {'values': '1 :label1, 2: label2, 3:label3', 'unit': None}
			, "[ 1 :label1 ,2: label2 ,3:label3 ]": {'values': '1 :label1 ,2: label2 ,3:label3', 'unit': None}
			, "[ 1 :label1 , 2: label2 , 3:label3 ]": {'values': '1 :label1 , 2: label2 , 3:label3', 'unit': None}
			
			, "[ 1:label1 ](mm) ": {'unit': 'mm', 'values': '1:label1'}
			, "[ 1:label1 ]( mm) ": {'unit': 'mm', 'values': '1:label1'}
			, "[ 1:label1 ]( mm ) ": {'unit': 'mm', 'values': '1:label1'}
			, "[ 1:label1 ](mm ) ": {'unit': 'mm', 'values': '1:label1'}
			, "[ 1:label1 ] ( mm ) ": {'unit': 'mm', 'values': '1:label1'}
			, "[ 1:label1 ] (mm ) ": {'unit': 'mm', 'values': '1:label1'}
			, "[ 1:label1 ] ( mm) ": {'unit': 'mm', 'values': '1:label1'}
			, "[ 1:label1 ] (mm) ": {'unit': 'mm', 'values': '1:label1'}

		}
	}
	, "values_number_schema_re":{
		"regex": openscad.values_number_schema_re
		, "tests":{
			  "": None
			, " ": None
			, "[]": None
			, " [ ] ": None
			, " [] ": None
			, "[] ": None
			, " []": None
			, "[]": None
			, "[ value1, value2, value3 ]": None
			, "[value1,value2,value3]": None
			, "[value1, value2, value3 ]": None
			, "[ value1 , value2 , value3 ]": None
			, "[value1:, value2, value3 ]": None
			, "[ value1: , value2 , value3 ]": None
			, "[1,2,3]": {'values': '1,2,3', 'unit': None}
			, "[ 1,2,3]": {'values': '1,2,3', 'unit': None}
			, "[1,2,3 ]": {'values': '1,2,3', 'unit': None}
			, "[ 1,2,3 ]": {'values': '1,2,3', 'unit': None}
			, "[ 1, 2 ,3 ]": {'values': '1, 2 ,3', 'unit': None}
			, "[1, 2 ,3]": {'values': '1, 2 ,3', 'unit': None}
			, "[1.0,2.0,3.0]": {'values': '1.0,2.0,3.0', 'unit': None}
			, "[ 1.0,2.0,3.0]": {'values': '1.0,2.0,3.0', 'unit': None}
			, "[1.0,2.0,3.0 ]": {'values': '1.0,2.0,3.0', 'unit': None}
			, "[ 1.0,2.0,3.0 ]": {'values': '1.0,2.0,3.0', 'unit': None}
			, "[ 1.0, 2.0 ,3.0 ]": {'values': '1.0, 2.0 ,3.0', 'unit': None}
			, "[1.0, 2.0 ,3.0]": {'values': '1.0, 2.0 ,3.0', 'unit': None}
			, "[-1.0,-2.0,-3.0]": {'values': '-1.0,-2.0,-3.0', 'unit': None}
			, "[ -1.0,-2.0,-3.0]": {'values': '-1.0,-2.0,-3.0', 'unit': None}
			, "[-1.0,-2.0,-3.0 ]": {'values': '-1.0,-2.0,-3.0', 'unit': None}
			, "[ -1.0,-2.0,-3.0 ]": {'values': '-1.0,-2.0,-3.0', 'unit': None}
			, "[ -1.0, -2.0 ,-3.0 ]": {'values': '-1.0, -2.0 ,-3.0', 'unit': None}
			, "[-1.0, -2.0 ,-3.0]": {'values': '-1.0, -2.0 ,-3.0', 'unit': None}
			, "[-1.0, -2.0 ,-3.0,-1.0, -2.0 ,-3.0]": {'values': '-1.0, -2.0 ,-3.0,-1.0, -2.0 ,-3.0', 'unit': None}
			, "[1,2,3](mm)": {'values': '1,2,3', 'unit': 'mm'}
			, "[1,2,3]( mm)": {'values': '1,2,3', 'unit': 'mm'}
			, "[1,2,3]( mm )": {'values': '1,2,3', 'unit': 'mm'}
			, "[1,2,3](mm )": {'values': '1,2,3', 'unit': 'mm'}
			, "[1,2,3] ( mm )": {'values': '1,2,3', 'unit': 'mm'}
			, "[1,2,3] (mm )": {'values': '1,2,3', 'unit': 'mm'}
			, "[1,2,3] ( mm)": {'values': '1,2,3', 'unit': 'mm'}
			, "[1,2,3] (mm)": {'values': '1,2,3', 'unit': 'mm'}
			, "[1,2,3](mm) ": {'values': '1,2,3', 'unit': 'mm'}
			, "[1,2,3]( mm) ": {'values': '1,2,3', 'unit': 'mm'}
			, "[1,2,3]( mm ) ": {'values': '1,2,3', 'unit': 'mm'}
			, "[1,2,3](mm ) ": {'values': '1,2,3', 'unit': 'mm'}
			, "[1,2,3] ( mm ) ": {'values': '1,2,3', 'unit': 'mm'}
			, "[1,2,3] (mm ) ": {'values': '1,2,3', 'unit': 'mm'}
			, "[1,2,3] ( mm) ": {'values': '1,2,3', 'unit': 'mm'}
			, "[1,2,3] (mm) ": {'values': '1,2,3', 'unit': 'mm'}
			, "[ 1,2,3] ( mm ) ": {'values': '1,2,3', 'unit': 'mm'}
			, "[ 1.0,2.0,3.0 ] ( mm ) ": {'values': '1.0,2.0,3.0', 'unit': 'mm'}
			, "[ 1.0, 2.0 ,3.0 ] ( mm ) ": {'values': '1.0, 2.0 ,3.0', 'unit': 'mm'}
			, "[1.0, 2.0 ,3.0] ( mm ) ": {'values': '1.0, 2.0 ,3.0', 'unit': 'mm'}
			, "[-1.0,-2.0,-3.0] ( mm ) ": {'values': '-1.0,-2.0,-3.0', 'unit': 'mm'}
			, "[ -1.0, -2.0 ,-3.0 ] ( mm ) ": {'values': '-1.0, -2.0 ,-3.0', 'unit': 'mm'}
			, "[-1.0, -2.0 ,-3.0] ( mm ) ": {'values': '-1.0, -2.0 ,-3.0', 'unit': 'mm'}
			, "[-1.0, -2.0 ,-3.0,-1.0, -2.0 ,-3.0] ( mm ) ": {'values': '-1.0, -2.0 ,-3.0,-1.0, -2.0 ,-3.0', 'unit': 'mm'}
		}
	}
	
	
	
}


def test_regexes():
	for name, case in regexes.items():
		tests = case.get("tests")
		regex = case.get("regex")
		if tests and regex:
			logger.info(f"----------------------------------------------------- {name} ({regex})")
			for test, expected in tests.items():
				m = regex.match(test)
				actual = m and m.groupdict()
				logger.info(f" + '{test}': {pprint.pformat(expected)} vs. {pprint.pformat(actual)}")
				assert actual == expected, f"For test {name}: '{test}'"
		else:
			logger.warn(f"Problem in regex '{name}' ({regex}) or it's tests '{pprint.pformat(tests)}', skipping...")
			

def test_one():
	source = """
/* [Drop down box] */
// labeled combo box for numbers
Labeled_values=10; // [10:L, 20:M, 30:XL]
"""
	expected_schema = [{'default': {'type': 'number', 'value': 10},
	'description': 'labeled combo box for numbers',
	'name': 'Labeled_values',
	'schema': {'labels': {10: 'L', 20: 'M', 30: 'XL'},
			   'raw': '[10:L, 20:M, 30:XL]'},
	'section': 'Drop down box',
	'unit':None
	}]
	schema = openscad.parse_customize(source, do_debug = False)
	if expected_schema:
		logger.info("ONE -------------------------------------------------\n"+source+"\n")
		logger.info("SCHEMA:\n\n"+pprint.pformat(schema)+"\n")
		logger.info("EXPECTED:\n\n"+pprint.pformat(expected_schema)+"\n")
		assert(expected_schema == schema)
	



