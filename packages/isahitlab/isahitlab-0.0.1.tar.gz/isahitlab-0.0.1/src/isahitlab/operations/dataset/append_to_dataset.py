import uuid
import logging
import json
from tqdm import tqdm
from typing import List, Optional, Iterable, Dict, Union
from isahitlab.helpers.resource import is_url, is_resource
from isahitlab.helpers.list import list_duplicates, remove_duplicates
from isahitlab.operations.base import BaseAction
from isahitlab.api.dataset.api import DatasetApi
from isahitlab.domain.dataset import FilePayload, DatasetId
from isahitlab.domain.batch import BatchId
from isahitlab.domain.project import ProjectId

from typeguard import typechecked

logger = logging.getLogger('isahitlab.append_to_dataset')


class AppendToDatasetOperation(BaseAction):
    """Upload files to a dataset

    """


    _dataset_api : DatasetApi

    @typechecked
    def run(
        self,
        project_id: ProjectId,
        dataset_id: BatchId,
        files: List[FilePayload],
        disable_progress_bar: Optional[bool] = False,
    ) -> Iterable[Dict]:
        """ Add resources to a dataset
        
            project_id: ID of the project
            dataset_id: ID of the dataset_id
                You can also provide a batch_id to use the dataset linked to the batch
            batch_id: ID of the batch
            files : list of the file to create, str or Dict -> FilePayload(path : str, file : str)
            disable_progress_bar: Disable the progress bar display
        """
        self._dataset_api = DatasetApi(self._http_client)
        nb_files = len(files)
        
        with tqdm(total=nb_files,  disable=disable_progress_bar, desc="Uploading files... ") as loader:
            for file in files:
                self._upload_file(file.file, file.path, dataset_id, project_id)
                loader.update(1)
            

        tasks = []
        
        return tasks
    
    def _upload_file(self, resource: str, folder: str, dataset_id: DatasetId, project_id: ProjectId) -> Dict:
        with open(resource, 'rb') as f:
            file_info = self._dataset_api.upload_file(dataset_id=dataset_id, project_id=project_id, file=f, folder=folder)
        return file_info

