# SPDX-FileCopyrightText: 2024-present Benjamin Piogé <benjamin@isahit.com>
#
# SPDX-License-Identifier: MIT

from typing import Literal, Dict, List, Any, Optional
from jsonschema import validate
from jsonschema import Draft202012Validator
from isahitlab.domain.task import TaskPayload, TaskCompatibilityMode
from isahitlab.domain.project import ProjectType
from . import validation_schemas
from .form_validation_builder import build_validation_schema_for_form

ValidationSchema = Literal['lab_iat']


def validate_task_payloads(tasks: List[TaskPayload],  project_configuration: Dict[str, Any], compatibility_mode: Optional[TaskCompatibilityMode] = None) -> True:
    validation_schema = None

    project_type : ProjectType =  project_configuration['projectType']
    
    # Select schema
    if compatibility_mode == "kili":
        validation_schema = validation_schemas.KILI_SCHEMA        
    elif project_type == "iat-rectangle":
        validation_schema = validation_schemas.LAB_IAT_RECTANGLE_SCHEMA
    elif project_type == "iat-segmentation":
        validation_schema = validation_schemas.LAB_IAT_SEGMENTATION_SCHEMA
    elif project_type in ["iat-polygon", "iat-graph", "iat-polyline"]:
        validation_schema = validation_schemas.LAB_IAT_SCHEMA
    elif project_type == "form":
        validation_schema = build_validation_schema_for_form(project_configuration=project_configuration)
    

    if not validation_schema:
        raise Exception('Validation Schema not found for {}'.format(project_type))
    

    Draft202012Validator.check_schema(validation_schema)

    draft_202012_validator = Draft202012Validator(validation_schema)

    for task in tasks:
        if task.data:
            draft_202012_validator.validate(task.data)

