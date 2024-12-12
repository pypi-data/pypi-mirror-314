from tqdm import tqdm
from typing import List, Optional, Iterable, Dict, cast
from isahitlab.actions.base import BaseAction
from isahitlab.api.task.api import TaskApi
from isahitlab.api.project_configuration.api import ProjectConfigurationApi
from isahitlab.domain.task import TaskFilters, TaskStatus, TaskOptionalFields, TaskId, TaskCompatibilityMode
from isahitlab.domain.batch import BatchId
from isahitlab.operations.project_configuration.get_project_configuration import GetProjectConfigurationOperation
from isahitlab.formatters import get_compatibility_formatter

from typeguard import typechecked

class ProjectConfigurationActions(BaseAction):
    """Project configuration actions"""

    @typechecked
    def project_configuration(
        self,
        project_id: str,
        disable_progress_bar: Optional[bool] = False
    ) -> Dict:
        """ Get the configuration of a project
        
        Args:
            project_id: ID of the project
            disable_progress_bar: Disable the progress bar display

        """

        operation = GetProjectConfigurationOperation(self.http_client)

        return operation.run(project_id=project_id, disable_progress_bar=disable_progress_bar)

    