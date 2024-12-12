KILI_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "OBJECT_DETECTION_JOB": {
            "type": "object",
            "properties": { 
                "annotations" : {
                    "type" : "array",
                    "items" : {
                        "type" : "object",
                        "properties" : {
                            "boundingPoly": {
                                "type" : "array",
                                "minContains" : 1,
                                "items" : {
                                    "type" : "object",
                                    "properties" : {
                                        "normalizedVertices" : {
                                            "type" : "array",
                                            "items" : {
                                                "type" : "object",
                                                "properties" : {
                                                    "x" : { 
                                                        "type": "number", 
                                                        "minimum": 0,
                                                        "exclusiveMaximum": 1 
                                                    },
                                                    "y" : { 
                                                        "type": "number", 
                                                        "minimum": 0,
                                                        "exclusiveMaximum": 1 
                                                    }
                                                },
                                                "required" : ["x", "y"]
                                            }
                                        },
                                        "vertices": {
                                            "type" : "array",
                                            "items" : {
                                                "type" : "object",
                                                "properties" : {
                                                    "x" : { "type": "number" },
                                                    "y" : { "type": "number" }
                                                },
                                                "required" : ["x", "y"]
                                            }
                                        }
                                    },
                                    "anyOf": [
                                        { "required" : ["normalizedVertices"] },
                                        { "required" : ["vertices"] },
                                    ]
                                }
                            },
                            "categories": {
                                "type" : "array",
                                "items" : {
                                    "type" : "object",
                                    "properties" : {
                                        "name" : { "type": "string" }
                                    }
                                }
                            }
                        },
                        "required" : ["boundingPoly"]
                    }
                }
            },
            "required": ["annotations"]
        },
        "resolution": {
          "width": { "type" : "number" },
          "height": { "type" : "number" }
        },
    },
    "required": ["OBJECT_DETECTION_JOB"],
    "$defs": {
        "annotation": {
            "type": "object",
            "properties": {
                "uid": {"type": "string"},
                "color": {"type": "string"},
                "text": {"type": "string"},
                "polygons": { "$ref": "#/$defs/polygons" },
                "labels" : { "$ref" : "#/$defs/labels" }
            },
            "required": ["polygons"],
        },
        "vertice": {
            "type": "number",
            "minimum": 0,
            "exclusiveMaximum": 1
        },
        "vertices": { 
            "type": "array", 
            "items": { "$ref" : "#/$defs/vertice" }
        },
        "polygon_type": {
            "const" : "polygon"
        },
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
                                    "vertices" : { "$ref" : "#/$defs/vertices"
                                    },
                                    "type" : { "$ref" : "#/$defs/polygon_type" }
                                },
                                "required": ["vertices", "type"],
                            },
                            "groupId" : { "type" : "string" },
                            "text" : { "type" : "string" },
                        },
                        "required": ["geometry"],
                    }
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
                        "children" : { "$ref" : "#/$defs/labels" }
                    },
                    "additionalProperties": False,
                }
            },
            "additionalProperties": False,
        }
    },
}