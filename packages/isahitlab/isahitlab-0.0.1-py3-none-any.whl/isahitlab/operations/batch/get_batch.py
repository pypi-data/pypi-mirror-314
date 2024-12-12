from tqdm import tqdm
from typing import Optional, Dict
from isahitlab.operations.base import BaseAction
from isahitlab.domain.batch import BatchId
from isahitlab.api.batch.api import BatchApi

from typeguard import typechecked

class GetBatchOperation(BaseAction):
    """Project configuration actions"""

    @typechecked
    def run(
        self,
        batch_id: BatchId,
        disable_progress_bar: Optional[bool] = False
    ) -> Dict:
        """ Get a batch by id
        
        Args:
            batch_id: ID of the batch
            disable_progress_bar: Disable the progress bar display
        """

        batch = None

        batch_api = BatchApi(self._http_client)
        with tqdm(total=1,  disable=disable_progress_bar, desc="Loading batch... ") as loader:
            batch = batch_api.get_batch_by_id(batch_id)
            loader.update(1)

        return batch
    