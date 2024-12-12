from typing import List, BinaryIO, Dict
from isahitlab.api.base import BaseApi
from ..helpers import get_response_json, log_raise_for_status

class DatasetApi(BaseApi):
    """Dataset API Calls"""
    

    def upload_file(self, project_id: str, dataset_id: str, file : BinaryIO, folder: str) -> Dict :
        """Upload file to dataset"""
        
        files = {'file': file }

        uploaded = self._http_client.post('api/file-manager/datasets/{}/resources'.format(dataset_id), files=files, params={ "projectId" : project_id }, data={ "path": folder })
        
        log_raise_for_status(uploaded)
        
        return get_response_json(uploaded)