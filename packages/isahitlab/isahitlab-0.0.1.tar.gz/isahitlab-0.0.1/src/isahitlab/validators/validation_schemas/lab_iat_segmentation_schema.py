from .lab_iat_schema import LAB_IAT_SCHEMA
import copy

LAB_IAT_SEGMENTATION_SCHEMA = copy.deepcopy(LAB_IAT_SCHEMA)

# Enforce number of vertices
LAB_IAT_SEGMENTATION_SCHEMA["properties"]["annotations"]["items"]["properties"]["polygons"] = { 
    "type": "array", 
    "prefixItems": [
        { "type" : "number" },
        { "type" : "number" },
        { "type" : "number" },
    ]
}

# Add mask
LAB_IAT_SEGMENTATION_SCHEMA["properties"]["mask"] = {
    "type" : "string",
    "pattern": "^data:image/png;base64,"
}