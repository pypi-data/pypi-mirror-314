import warnings
from typing import List, Optional, Iterable, Dict, cast
from isahitlab.actions.base import BaseAction
from isahitlab.operations.task.get_tasks import GetTasksOperation
from isahitlab.operations.task.create_tasks import CreateTask
from isahitlab.operations.project.get_projects import GetProjectsOperation
from isahitlab.domain.task import TaskFilters, TaskStatus, TaskOptionalFields, TaskId, TaskCompatibilityMode, TaskPayload
from isahitlab.domain.batch import BatchId
from isahitlab.domain.project import ProjectId, ProjectFilters, ProjectType

from typeguard import typechecked

class TaskActions(BaseAction):
    """Tasks actions"""

    @typechecked
    def tasks(
        self,
        project_id: ProjectId,
        batch_ids: Optional[List[str]] = None,
        status_in: Optional[List[str]] = None,
        task_id_in: Optional[List[str]] = None,
        name_in: Optional[List[str]] = None,
        name_like: Optional[str] = None,
        created_at_gt: Optional[str] = None,
        created_at_gte: Optional[str] = None,
        created_at_lt: Optional[str] = None,
        created_at_lte: Optional[str] = None,
        updated_at_gt: Optional[str] = None,
        updated_at_gte: Optional[str] = None,
        updated_at_lt: Optional[str] = None,
        updated_at_lte: Optional[str] = None,
        optional_fields: Optional[List[TaskOptionalFields]] = ["data"],
        disable_progress_bar: Optional[bool] = False,
        compatibility_mode: Optional[TaskCompatibilityMode] = None
    ) -> Iterable[Dict]:
        """ Get an task list
        
        Args:
            project_id: ID of the project
            batch_ids: A list of batch ids to filter
            status_in: Only in those statuses.
                Possible choices: `pending`, `complete`, `configuring`.
            task_id_in: Only task whose ID is in this list,
            name_in: Only task whose name is in this list,
            name_like: Only task whose name mathes this regex,
            created_at_gt: Only tasks created after this date (Ex.: "2022-09-19 08:30:00")
            created_at_gte: Only tasks created at or after this date (Ex.: "2022-09-19 08:30:00")
            created_at_lt: Only tasks created before this date (Ex.: "2022-09-19 08:30:00")
            created_at_lte: Only tasks created at or before this date (Ex.: "2022-09-19 08:30:00")
            updated_at_gt: Only tasks updated after this date (Ex.: "2022-09-19 08:30:00")
            updated_at_gte: Only tasks updated at or after this date (Ex.: "2022-09-19 08:30:00")
            updated_at_lt: Only tasks updated before this date (Ex.: "2022-09-19 08:30:00")
            updated_at_lte: Only tasks updated at or before this date (Ex.: "2022-09-19 08:30:00")
            optional_fields: retreive those additional information
                Possible choices: `data`, `jobs`, `metrics`, `data.mask`(for segmentation project).
            disable_progress_bar: Disable the progress bar display
            compatibility_mode: Format the output for specific use cases
                Possible choices: `kili` -> format the ouput to look like kili.assets() results 

        """

        filters = TaskFilters(
            project_id=project_id, 
            batch_id_in = cast(List[BatchId], batch_ids) if batch_ids else None,
            status_in = cast(List[TaskStatus], status_in) if status_in else None,
            task_id_in = cast(List[TaskId], task_id_in) if task_id_in else None,
            name_in = cast(List[str], name_in) if name_in else None,
            name_like = name_like if name_like else None,
            created_at_gt = cast(List[str], created_at_gt) if created_at_gt else None,
            created_at_gte = cast(List[str], created_at_gte) if created_at_gte else None,
            created_at_lt = cast(List[str], created_at_lt) if created_at_lt else None,
            created_at_lte = cast(List[str], created_at_lte) if created_at_lte else None,
            updated_at_gt = cast(List[str], updated_at_gt) if updated_at_gt else None,
            updated_at_gte = cast(List[str], updated_at_gte) if updated_at_gte else None,
            updated_at_lt = cast(List[str], updated_at_lt) if updated_at_lt else None,
            updated_at_lte = cast(List[str], updated_at_lte) if updated_at_lte else None,
            optional_fields = cast(List[TaskOptionalFields], optional_fields) if optional_fields else None
        )
        
        operation = GetTasksOperation(self.http_client)

        return operation.run(project_id=project_id, filters=filters, disable_progress_bar=disable_progress_bar, compatibility_mode=compatibility_mode )
    

    @typechecked
    def create_tasks(
        self,
        project_id: str,
        batch_id: str,
        tasks: List[Dict],
        disable_progress_bar: Optional[bool] = False,
        disable_data_check: Optional[bool] = False,
        disable_unicity_check: Optional[bool] = False,
        raise_if_existing: Optional[bool] = True,
        compatibility_mode: Optional[TaskCompatibilityMode] = None
    ) -> Iterable[Dict]:
        """ Create tasks in a batch
        
        Args:
            project_id: ID of the project
            batch_id: ID of the batch project
            tasks : list of the tasks to create. See TaskPayload(name : str, resource : str, data : Dict[str, Any])
            disable_progress_bar: Disable the progress bar display
            disable_data_check: Set this option to False to ignore the data format validation
            disable_unicity_check: Set this option to True to ignore duplicate check and insert it anyway
            raise_if_existing: Set this option to False to skip task duplicates and only show a warning
            compatibility_mode: Format the output for specific use cases
                Possible choices: `kili` -> format the ouput to look like kili.assets() results 

        """

        projects = GetProjectsOperation(self.http_client).run(filters=ProjectFilters(id_in=[project_id]), disable_progress_bar=disable_progress_bar)
        project = projects[0] if len(projects) > 0 else None

        if not project:
            warnings.warn('Project not found')
            return

        project_type : ProjectType = project['type']

        operation = CreateTask(self.http_client)
        task_payloads = [*map(lambda t: TaskPayload(
            name=t['name'],
            resources=t['resources'] if project_type != "form" else None,
            data=t['data'] if 'data' in t else None
            ), tasks)]
        
        tasks = operation.run(project_id=project_id,
                        batch_id=batch_id,
                        tasks=task_payloads, 
                        disable_progress_bar=disable_progress_bar, 
                        disable_unicity_check=disable_unicity_check,
                        raise_if_existing=raise_if_existing,
                        disable_data_check=disable_data_check,
                        compatibility_mode=compatibility_mode
                        )       
        
        return tasks
    