from tqdm import tqdm
from typing import Optional, Dict,List
from isahitlab.operations.base import BaseAction
from isahitlab.domain.project import ProjectFilters
from isahitlab.api.project.api import ProjectApi

from typeguard import typechecked

class GetProjectsOperation(BaseAction):
    """Get project actions"""

    @typechecked
    def run(
        self,
        filters: ProjectFilters,
        disable_progress_bar: Optional[bool] = False
    ) -> List[Dict]:
        """ Get the configuration of a project
        
        Args:
            filters : ProjectFilters object
            disable_progress_bar: Disable the progress bar display
        """

        projects = []

        project_api = ProjectApi(self._http_client)
        with tqdm(total=1,  disable=disable_progress_bar, desc="Loading projects... ") as loader:
             for (docs, loaded, total) in project_api.get_all_projects(filters):
                loader.total = total
                projects = projects + docs
                loader.update(loaded - loader.n)

        return projects
    