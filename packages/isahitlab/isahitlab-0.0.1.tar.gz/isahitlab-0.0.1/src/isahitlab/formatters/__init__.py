# SPDX-FileCopyrightText: 2024-present Benjamin Piogé <benjamin@isahit.com>
#
# SPDX-License-Identifier: MIT
from typing import Dict
from isahitlab.domain.task import TaskCompatibilityMode
from .lab_to_kili_formatter import LabToKiliFormatter
from .kili_to_lab_formatter import KiliToLabFormatter
from .base import BaseFormatter

def get_compatibility_formatter(from_mode : TaskCompatibilityMode, to_mode : TaskCompatibilityMode, project_configuration : Dict) -> BaseFormatter :
    """Factory"""
    if from_mode == "lab" and to_mode == "kili":
        return LabToKiliFormatter(project_configuration)
    if from_mode == "kili" and to_mode == "lab":
        return KiliToLabFormatter(project_configuration)
