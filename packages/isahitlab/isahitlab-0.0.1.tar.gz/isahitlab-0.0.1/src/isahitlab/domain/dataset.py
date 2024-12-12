from typing import NewType, Union
from dataclasses import dataclass

DatasetId = NewType("DatasetId", str)

@dataclass
class FilePayload(dict):
    """Task payload for task create

    Inherit from dict to make it JSON serializable
    
    Args:
        file: Name of the task (appended to the path, it must be unique in a dataset)
        path: Path of a resource (ex.: "./images/image1.jpg")
    """

    file: str
    path:  Union[str, None]
    

    def __init__(self, file, path):
        self.file = file
        self.path = path
        dict.__init__(self, file=file, path=path)
