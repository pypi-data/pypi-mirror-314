from tqdm import tqdm
from typing import List, Optional, Iterable, Dict, cast
from isahitlab.operations.base import BaseAction
from isahitlab.api.task.api import TaskApi
from isahitlab.api.project_configuration.api import ProjectConfigurationApi
from isahitlab.domain.task import TaskFilters, TaskCompatibilityMode
from isahitlab.domain.project import ProjectId
from isahitlab.formatters import get_compatibility_formatter

from typeguard import typechecked

class GetTasksOperation(BaseAction):
    """Tasks actions"""

    @typechecked
    def run(
        self,
        project_id: ProjectId,
        filters: TaskFilters,
        disable_progress_bar: Optional[bool] = False,
        compatibility_mode: Optional[TaskCompatibilityMode] = None
    ) -> Iterable[Dict]:
        """ Get an task list
        
        Args:
            project_id: ID of the project
            filters : TaskFilters object
            disable_progress_bar: Disable the progress bar display
            compatibility_mode: Format the output for specific use cases
                Possible choices: `kili` -> format the ouput to look like kili.assets() results 

        """
        task_api = TaskApi(self._http_client)

        tasks = []
        
        # Load configuration and initialize the formatter if required
        formatter = None
        if compatibility_mode:
            project_configuration_api = ProjectConfigurationApi(self._http_client)
            with tqdm(total=1,  disable=disable_progress_bar, desc="Loading project configuration... ") as loader:
                project_configuration = project_configuration_api.get_project_configuration(project_id)
                loader.update(1)            
            formatter = get_compatibility_formatter("lab", compatibility_mode, project_configuration)

        # load and format task
        with tqdm(total=0,  disable=disable_progress_bar, desc="Loading tasks... ") as loader:
            for (docs, loaded, total) in task_api.get_all_tasks(filters):
                loader.total = total
                if formatter :
                    docs = formatter.format_tasks(docs)
                tasks = tasks + docs
                loader.update(loaded - loader.n)

        return tasks
    
