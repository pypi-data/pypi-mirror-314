import uuid
import logging
import json
from tqdm import tqdm
from typing import List, Optional, Iterable, Dict, Union
from isahitlab.helpers.resource import is_url, is_resource
from isahitlab.helpers.list import list_duplicates, remove_duplicates
from isahitlab.operations.base import BaseAction
from isahitlab.api.task.api import TaskApi
from isahitlab.api.file.api import FileApi
from isahitlab.api.data.api import DataApi
from isahitlab.api.project_configuration.api import ProjectConfigurationApi
from isahitlab.formatters import get_compatibility_formatter
from isahitlab.domain.task import TaskCompatibilityMode, TaskPayload
from isahitlab.domain.batch import BatchId
from isahitlab.domain.project import ProjectId
from isahitlab.validators import validate_task_payloads

from typeguard import typechecked

logger = logging.getLogger('isahitlab.create_task')


class CreateTask(BaseAction):
    """Create task actions
    """


    _task_api : TaskApi
    _file_api : FileApi
    _data_api : DataApi

    @typechecked
    def run(
        self,
        project_id: ProjectId,
        batch_id: BatchId,
        tasks: List[TaskPayload],
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
        self._task_api = TaskApi(self._http_client)
        self._file_api = FileApi(self._http_client)
        self._data_api = DataApi(self._http_client)
        project_configuration_api = ProjectConfigurationApi(self._http_client)
        
        project_configuration = None
        
        formatter = None

        if compatibility_mode:
            project_configuration = project_configuration_api.get_project_configuration(project_id=project_id) if project_configuration == None else project_configuration
            formatter = get_compatibility_formatter(compatibility_mode, "lab", project_configuration)
            validate_task_payloads(tasks, project_configuration, compatibility_mode)
            tasks = formatter.format_tasks(tasks)

        if not disable_data_check:
            # Check data against configuration
            project_configuration = project_configuration_api.get_project_configuration(project_id=project_id) if project_configuration == None else project_configuration
            validate_task_payloads(tasks, project_configuration, compatibility_mode)

        if not disable_unicity_check:
            tasks = self._check_unicity_and_filter(batch_id=batch_id,raise_if_existing=raise_if_existing,tasks=tasks)
            
        nb_tasks = len(tasks)
        created = []
        
        with tqdm(total=nb_tasks,  disable=disable_progress_bar, desc="Creating tasks... ") as loader:
            for task in tasks:
                created.append(self._create_task(batch_id, task))
                loader.update(1)
            

        
        return created
    

    def _check_unicity_and_filter(self, batch_id: BatchId, raise_if_existing: bool, tasks : List[TaskPayload]) ->  List[TaskPayload]:
        # Check unicity
        task_names = [*map(lambda t : t.name, tasks)]
        
        # Check if two or more tasks have the same name
        dupes = list_duplicates(task_names)
        nb_dupes = len(dupes)
        if nb_dupes > 0:
            raise Exception(
"""You have {} duplicate task name(s): {}{}
    Set disable_unicity_check option to True to ignore this error
""".format(str(nb_dupes), ','.join(dupes[0:3]), " and {} more".format(str(nb_dupes - 3)) if nb_dupes > 3 else '')
            )

        # Check tasks with the same name exits in the batch
        existings = remove_duplicates(self._task_api.get_existing_task_names(batch_id=batch_id, names=task_names))
        if len(existings):
            nb_existings = len(existings)
            existings_message = "{} task name(s) already exist in your batch: {}{}".format(str(nb_existings), ','.join(existings[0:3]), " and {} more".format(str(nb_existings - 3)) if nb_existings > 3 else '')
            if raise_if_existing:
                raise Exception(
"""{}
    Set raise_if_existing option to False to skip these tasks and only show a warning
    Set disable_unicity_check option to True to ignore and insert it anyway
""".format(existings_message))
            else:
                logger.debug('debug')
                logger.warning(
"""{}
    Set disable_unicity_check option to True to ignore and insert it anyway
""".format(existings_message))
                tasks = list(filter(lambda t: t.name not in existings, tasks))
        return tasks
    
    def _create_task(self, batch_id: str, task : TaskPayload) -> str:
        resources = []
        grant_resources_token = None
        data_id = None
        grant_data_token = None

        # Handle resources
        if task.resources:
            (resources, grant_resources_token) = self._create_resources(batch_id=batch_id, resources=task.resources)

        # Handle data
        if task.data:
            (data_id, grant_data_token) = self._create_data(batch_id=batch_id, name=task.name, data=task.data)


        # Finally, create the taks
        return self._task_api.create_task(batch_id=batch_id, name=task.name, resources=resources, data_id=data_id, grant_resources=grant_resources_token, grant_data=grant_data_token)


    def _upload_file(self, resource: str, folder: str, batch_id: str) -> Dict:
        with open(resource, 'rb') as f:
            file_info = self._file_api.upload_file(batch_id=batch_id, file=f, folder=folder)
        return file_info


    def _create_resources(self, batch_id: str, resources: List[Union[str,Dict]]) -> tuple[List[Union[str,Dict]], str]:
        normalized_resources = []
        file_ids = []
        for resource in resources:
            if not is_url(resource) and not is_resource(resource):
                # Assume it is a local file
                folder = str(uuid.uuid4())
                file_info = self._upload_file(resource, folder, batch_id)
                file_ids.append(file_info['_id'])
                normalized_resources.append({
                    "id": file_info['_id'], 
                    "name":  file_info["name"]
                })
            else:
                normalized_resources.append(resource)
        grant_resources_token = None
        if len(file_ids):
            grant_resources_token = self._file_api.grant_file_access(ids=file_ids)["accessToken"]
        
        return (normalized_resources, grant_resources_token)
    
    def _create_data(self, batch_id: str, data: Dict, name: str) -> tuple[str, str]:
        data_result = self._data_api.import_data(batch_id=batch_id,name=name, body=data)
        data_id = data_result['initialDataId']
        grant_data_token = data_result['accessToken']
        return (data_id, grant_data_token)