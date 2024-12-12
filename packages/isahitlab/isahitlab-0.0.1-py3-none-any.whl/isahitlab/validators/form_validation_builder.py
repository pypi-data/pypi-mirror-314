"""Validation for form"""

from typing import Dict, Any
import copy
from isahitlab.helpers.inputs_layout import extract_not_static_inputs_from_layout
from . import validation_schemas

def build_validation_schema_for_form(project_configuration) ->  Dict[str, Any]:

    inputs_layout = project_configuration.get('metadata', {}).get('inputsLayout', None)

    if not inputs_layout:
        raise Exception('Not layout defined for the project')
    
    inputs = extract_not_static_inputs_from_layout(inputs_layout)

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
        },
        "patternProperties": {
            "^meta_": {}
        },
        "additionalProperties": False,
    }

    for input in inputs:
        schema["properties"][input["id"]] = _get_schema_for_input(input)

    return schema

    
def _get_schema_for_input(input: Dict[str, Any]) -> Dict[str, Any]:
    type = input['type']

    match type:
        case 'checkbox' : return { "oneOf" : [ { "type" : "string" }, { "type" : "number" }]}
        case 'date' : return { "type" : "string" }
        case 'display-resource-carousel' : return { "oneOf" : [ { "type" : "string" }, { "type" : "array", "items" : { "type" : "string" }} ] }
        case 'display-resource' : return { "oneOf" : [ { "type" : "string" }, { "type" : "array", "items" : { "type" : "string" }} ] }
        case 'display-text' : return { "type" : "string" }
        case 'display-title' : return { "type" : "string" }
        case 'email' : return { "type" : "string" }
        case 'hidden' : return { "type" : "string" }
        case 'listbox' : return {}
        case 'number' : return { "type" : "number" }
        case 'radio' : return { "oneOf" : [ { "type" : "string" }, { "type" : "number" }]}
        case 'text' : return { "oneOf" : [ { "type" : "string" }, { "type" : "number" }]}
        case 'textarea' : return { "oneOf" : [ { "type" : "string" }, { "type" : "number" }]}
        case 'tool-iat-rectangle' : return _get_iat_with_resource(validation_schemas.LAB_IAT_RECTANGLE_SCHEMA)
        case 'tool-iat-polygon' : return _get_iat_with_resource(validation_schemas.LAB_IAT_SCHEMA)
        case 'tool-iat-polyline' : return _get_iat_with_resource(validation_schemas.LAB_IAT_SCHEMA)
        case 'tool-iat-graph' : return _get_iat_with_resource(validation_schemas.LAB_IAT_SCHEMA)
        case 'tool-iat-segmentation' : return _get_iat_with_resource(validation_schemas.LAB_IAT_SEGMENTATION_SCHEMA)
        case 'url' : return { "oneOf" : [ { "type" : "string" }, { "type" : "number" }]}
        case 'display-json' : return {}
        case 'json-editor' : return {}
    
    return {}
    


def _get_iat_with_resource(schema: Dict[str, Any]) -> Dict[str, Any]:
    schema_copy = copy.deepcopy(schema)
    schema_copy["properties"]["resources"] = { "oneOf" : [ { "type" : "string" }, { "type" : "array", "items" : { "type" : "string" }} ] }
    return schema_copy