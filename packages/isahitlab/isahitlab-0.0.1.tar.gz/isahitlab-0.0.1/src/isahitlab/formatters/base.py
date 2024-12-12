from abc import ABC, abstractmethod
from typing import List, Dict


class BaseFormatter(ABC):
    """Base class for all formatter."""

    @abstractmethod
    def format_tasks(self, tasks: List[Dict]) -> List[Dict]:
        raise NotImplementedError