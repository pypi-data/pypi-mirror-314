from typing import Dict
from isahitlab.api.base import BaseApi
from isahitlab.domain.batch import BatchId
from ..helpers import get_response_json, log_raise_for_status

class BatchApi(BaseApi):
    """Batch API Calls"""

    def get_batch_by_id(self, batch_id : BatchId) -> Dict :
        """Get batch"""

        project_configuration = self._http_client.get('api/task-manager/batches/{}'.format(batch_id))

        log_raise_for_status(project_configuration)

        return get_response_json(project_configuration)
