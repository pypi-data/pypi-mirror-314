from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional, Union


MIMETYPE_OPENSCAD_MODEL:str = "model/openscad"
MIMETYPE_NTOP_MODEL:str = "model/ntop"
MIMETYPE_STL_MODEL:str = "model/stl"
MIMETYPE_PNG_IMAGE:str = "image/png"
MIMETYPE_JSON_DATA:str = "application/json"
MIMETYPE_TEXT:str = "text/plain"


class ParameterTypeEnum(str, Enum):
	NUMBER = 'NUMBER'
	STRING = 'STRING'
	BOOL = 'BOOL'
 
class NumericGeneratorParameter(BaseModel):
	name:str = "Numeric parameter name"
	value:Union[int, float]
 
class StringGeneratorParameter(BaseModel):
	name:str = "String parameter name"
	value:str
	
class BoolGeneratorParameter(BaseModel):
	name:str = "Bool parameter name"
	value:bool
 
class GeneratorParameters(BaseModel):
	action: str
	parameters: List[Union[NumericGeneratorParameter, StringGeneratorParameter, BoolGeneratorParameter]]
 
class NumericRangeGeneratorParameterSchema(BaseModel):
	name:str = "Numeric parameter name"
	min: Optional[Union[int, float]]
	step: Optional[Union[int, float]]
	max: Optional[Union[int, float]]
	default: Optional[Union[int, float]]
	unit: Optional[str]
	description:Optional[str] = "Parameter description"
	section:Optional[str] = "Parameter section"
	type:ParameterTypeEnum = ParameterTypeEnum.NUMBER
 
 
class NumericLabelGeneratorParameterValue(BaseModel):
	name:str = "Numeric parameter label"
	value:Union[int, float]
	
class NumericLabelGeneratorParameterSchema(BaseModel):
	name:str = "Numeric parameter name"
	labels: Optional[List[NumericLabelGeneratorParameterValue]]
	default: Optional[Union[int, float]]
	unit: Optional[str]
	description:Optional[str] = "Parameter description"
	section:Optional[str] = "Parameter section"
	type:ParameterTypeEnum = ParameterTypeEnum.NUMBER
 
class StringLabelGeneratorParameterValue(BaseModel):
	name:str = "String parameter label"
	value:str
 
class StringLabelGeneratorParameterSchema(BaseModel):
	name:str = "String parameter name"
	labels: Optional[List[StringLabelGeneratorParameterValue]]
	default:Optional[str]
	description:Optional[str] = "Parameter description"
	section:Optional[str] = "Parameter section"
	type:ParameterTypeEnum = ParameterTypeEnum.STRING
 
class StringLiteralGeneratorParameterSchema(BaseModel):
	name:str = "String parameter name"
	default:Optional[str]
	description:Optional[str] = "Parameter description"
	section:Optional[str] = "Parameter section"
	type:ParameterTypeEnum = ParameterTypeEnum.STRING
 
class BoolGeneratorParameterSchema(BaseModel):
	name:str = "Boolean parameter name"
	default:bool = False
	description:Optional[str] = "Parameter description"
	section:Optional[str] = "Parameter section"
	type:ParameterTypeEnum = ParameterTypeEnum.BOOL
 
 
class GeneratorTypeEnum(str, Enum):
	openscad = 'openscad'
	ntop = 'ntop'
	unknown = 'unknown'
 
 
class GeneratorMeta(BaseModel):
	generator_type:GeneratorTypeEnum = GeneratorTypeEnum.unknown
	version:Optional[str] = None
	class Config:  
		use_enum_values = True  # Use strings to represent enums
 
class GeneratorParametersSchema(BaseModel):
	generator_meta:GeneratorMeta
	parameters:List[Union[
		NumericRangeGeneratorParameterSchema
		, NumericLabelGeneratorParameterSchema
		, StringLiteralGeneratorParameterSchema
		, StringLabelGeneratorParameterSchema
		, BoolGeneratorParameterSchema] ]
 
class GeneratorInput(BaseModel):
	id: str
	parameters:GeneratorParameters
	result_url:Optional[str] = None
 
class GeneratorOutput(BaseModel):
	id: str
	error: Optional[Union[str, dict]]
	parameters: GeneratorParameters
	model_url:Optional[str] = None
	thumbnail_url:Optional[str] = None
	log_url:Optional[str] = None
