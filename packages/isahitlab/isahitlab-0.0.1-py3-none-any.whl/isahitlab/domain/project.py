"""Project domain"""

from typing import NewType, Optional, List, Literal, Dict, Any
from .pagination import PaginationFilters
from dataclasses import dataclass

ProjectId = NewType("ProjectId", str)

ProjectType = Literal["form", "iat-rectangle", "iat-polygon", "iat-segmentation", "iat-graph", "iat-polyline"]
ProjectStatus = Literal["configuring", "pending", "complete", "toBeDeleted", "deleted", "archived"]


@dataclass
class ProjectFilters(PaginationFilters):
    """Project filters for running a project search."""
    id_in: Optional[ProjectId] = None
    status_in: Optional[List[ProjectStatus]] = None
    type_in: Optional[List[ProjectType]] = None
    search: Optional[str] = None
