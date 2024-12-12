
LAB_IAT_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "$id": "iat",
    "properties": {
        "annotations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "uid": {"type": "string"},
                    "color": {"type": "string"},
                    "text": {"type": "string"},
                    "polygons": {
                        "type": "array",
                        "items":  {
                            "type": "object",
                            "properties": {
                                "id":  {"type": "string"},
                                "color":  {"type": "string"},
                                "geometry":  {
                                    "type": "object",
                                    "properties":{
                                        "vertices" : { "$ref" : "iat#/$defs/polygon_vertices" },
                                        "type" : { "const" : "polygon" }
                                    },
                                    "required": ["vertices", "type"],
                                },
                                "groupId" : { "type" : "string" },
                                "text" : { "type" : "string" },
                            },
                            "required": ["geometry"],
                        }
                     },
                    "labels" : { "$ref" : "iat#/$defs/labels" }
                },
                "required": ["polygons"],
            }
        },
        "image": {
          "width": { "type" : "number" },
          "height": { "type" : "number" }
        },
    },
    "required": ["annotations"],
    "additionalProperties": False,
    "$defs": {
        "vertice": {
            "type": "number",
            "minimum": 0,
            "exclusiveMaximum": 1
        },
        "polygon_vertices": { 
            "type": "array", 
            "items": { "$ref" : "iat#/$defs/vertice" }
        },
        "rectangle_vertices": { 
            "type": "array", 
            "prefixItems": [
                { "$ref" : "iat#/$defs/vertice" },
                { "$ref" : "iat#/$defs/vertice" },
                { "$ref" : "iat#/$defs/vertice" },
                { "$ref" : "iat#/$defs/vertice" },
            ]
        },
        "labels": {
            "type": "object",
            "patternProperties": {
                "^[0-9a-zA-Z-_ ]+$": {
                    "type" : "object",
                    "properties":    {
                        "labels" : {
                            "type" : "array",
                            "items" : {
                                "type" : "object",
                                "properties": {
                                    "id" : { "type" : "string"},
                                    "name" : { "type" : "string"},
                                    "displayName" : {  "oneOf": [{"type" : "string"}, { "type" : "null"}]},
                                    "uid" : { "type" : "string"},
                                },
                                "required": ["id", "name"]
                            }
                        },
                        "children" : { "$ref" : "iat#/$defs/labels" }
                    },
                    "additionalProperties": False,
                }
            },
            "additionalProperties": False,
        }
    },
}