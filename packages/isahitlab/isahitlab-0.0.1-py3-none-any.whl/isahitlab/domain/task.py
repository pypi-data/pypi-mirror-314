"""Task domain"""

from dataclasses import dataclass
from typing import NewType, Optional, List, Literal, Dict, Any
from .project import ProjectId
from .batch import BatchId
from .pagination import PaginationFilters

TaskId = NewType("TaskId", str)


TaskStatus = Literal["pending", "complete", "configuring"]
TaskOptionalFields = Literal["metrics", "jobs", "data", "data.mask"]
TaskCompatibilityMode = Literal["kili", "lab"]

@dataclass
class TaskPayload(dict):
    """Task payload for task create

    Inherit from dict to make it JSON serializable
    
    Args:
        name: Name of the task (should be unique in a batch)
        resource: Path or URL of a resource (ex.: "./images/image1.jpg", "https:://domain.com/image1.jpg")
        data: Initial data for the task (depends on project type and configuration)
    """

    name: str
    data: Dict[str, Any]
    resources: Optional[List[str]] = None
    

    def __init__(self, name, resources, data):
        self.name = name
        self.resources = resources
        self.data = data
        dict.__init__(self, name=name, resources=resources, data=data)

@dataclass
class TaskFilters(PaginationFilters):
    """Task filters for running a task search."""

    batch_id_in: Optional[List[BatchId]] = None
    project_id: Optional[ProjectId] = None
    status_in: Optional[List[TaskStatus]] = None
    task_id_in: Optional[List[TaskId]] = None
    name_in: Optional[List[str]] = None
    name_like: Optional[str] = None
    created_at_gt: Optional[str] = None
    created_at_gte: Optional[str] = None
    created_at_lt: Optional[str] = None
    created_at_lte: Optional[str] = None
    updated_at_gt: Optional[str] = None
    updated_at_gte: Optional[str] = None
    updated_at_lt: Optional[str] = None
    updated_at_lte: Optional[str] = None
    optional_fields: Optional[List[TaskOptionalFields]] = None
