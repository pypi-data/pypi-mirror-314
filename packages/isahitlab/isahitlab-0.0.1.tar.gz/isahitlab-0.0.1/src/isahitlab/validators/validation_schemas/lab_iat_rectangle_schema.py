from .lab_iat_schema import LAB_IAT_SCHEMA
import copy

LAB_IAT_RECTANGLE_SCHEMA = copy.deepcopy(LAB_IAT_SCHEMA)

# Enforce number of vertices
LAB_IAT_RECTANGLE_SCHEMA["properties"]["annotations"]["items"]["properties"]["polygons"]["items"]["properties"]["geometry"]["properties"]["vertices"] =  { "$ref" : "iat#/$defs/rectangle_vertices" }

# Enforce geometry type
LAB_IAT_RECTANGLE_SCHEMA["properties"]["annotations"]["items"]["properties"]["polygons"]["items"]["properties"]["geometry"]["properties"]["type"] = { "const" : "rectangle" }