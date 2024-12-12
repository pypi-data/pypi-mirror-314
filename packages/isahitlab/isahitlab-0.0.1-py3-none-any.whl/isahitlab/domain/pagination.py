"""Task domain"""
from typing import Optional
from dataclasses import dataclass



@dataclass
class PaginationFilters:
    """Pagination filters."""

    pagination: bool = True
    page: Optional[int] = 1
    limit: Optional[int] = 10
