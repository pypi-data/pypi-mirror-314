import warnings
from typing import List, Optional, Iterable, Dict, Union
from isahitlab.actions.base import BaseAction
from isahitlab.operations.dataset.append_to_dataset import AppendToDatasetOperation
from isahitlab.operations.batch.get_batch import GetBatchOperation
from isahitlab.domain.batch import BatchId
from isahitlab.domain.project import ProjectId
from isahitlab.domain.dataset import DatasetId, FilePayload

from typeguard import typechecked

class DatasetActions(BaseAction):
    """Dataset actions"""

    @typechecked
    def append_to_dataset(
        self,
        project_id: str,
        files: List[Union[Dict, str]],
        batch_id: Optional[str] = None,
        dataset_id: Optional[str] = None,
        disable_progress_bar: Optional[bool] = False,
    ) -> Iterable[Dict]:
        """ Add files to a dataset
        
        Args:
            project_id: ID of the project
            dataset_id: ID of the dataset_id
                You can also provide a batch_id to use the dataset linked to the batch
            batch_id: ID of the batch
            files : list of the file to create, str or Dict -> FilePayload(path : str, file : str)
            disable_progress_bar: Disable the progress bar display
        """

        if not dataset_id and not batch_id:
            raise ValueError(
                'You must provide a dataset_id or a batch_id'
            )
        
        # Get the dataset linked to the batch
        if not dataset_id:
            batch = GetBatchOperation(self.http_client).run(batch_id=batch_id, disable_progress_bar=disable_progress_bar)
            if not batch:
                raise ValueError("Batch not found")
            if batch['projectId'] != project_id:
                raise ValueError("batch_id is not a batch of the project")
            if not batch['dataset']:
                raise ValueError('The batch has no dataset')
            dataset_id = batch['dataset']['id']    
        
        if not dataset_id:
            raise ValueError("Unknown dataset")
        
        operation = AppendToDatasetOperation(self.http_client)

        file_payloads = [*map(lambda t: FilePayload(
            file=t['file'] if not isinstance(t, str) else t,
            path=self._format_path(t['path']) if not isinstance(t, str) else None
            ), files)]
        
        return operation.run(project_id=project_id,
                                dataset_id=dataset_id,
                                files=file_payloads, 
                                disable_progress_bar=disable_progress_bar
                                )
    
    def _format_path(self, path: str) -> str:
        if not path:
            return None
        path = path.strip().strip('/')
        
        if len(path) == 0:
            return None
        
        return path + '/'
        

    