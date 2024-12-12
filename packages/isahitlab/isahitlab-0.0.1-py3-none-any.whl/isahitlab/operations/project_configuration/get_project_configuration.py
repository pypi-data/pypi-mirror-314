from tqdm import tqdm
from typing import Optional, Dict
from isahitlab.operations.base import BaseAction
from isahitlab.api.project_configuration.api import ProjectConfigurationApi

from typeguard import typechecked

class GetProjectConfigurationOperation(BaseAction):
    """Project configuration actions"""

    @typechecked
    def run(
        self,
        project_id: str,
        disable_progress_bar: Optional[bool] = False
    ) -> Dict:
        """ Get the configuration of a project
        
        Args:
            project_id: ID of the project
            disable_progress_bar: Disable the progress bar display
        """

        project_configuration = None

        project_configuration_api = ProjectConfigurationApi(self._http_client)
        with tqdm(total=1,  disable=disable_progress_bar, desc="Loading project configuration... ") as loader:
            project_configuration = project_configuration_api.get_project_configuration(project_id)
            loader.update(1)

        return project_configuration
    