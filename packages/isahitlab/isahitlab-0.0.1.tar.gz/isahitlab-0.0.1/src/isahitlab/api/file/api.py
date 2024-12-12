from typing import List, BinaryIO, Dict
from isahitlab.api.base import BaseApi
from ..helpers import get_response_json, log_raise_for_status

class FileApi(BaseApi):
    """File API Calls"""

    def grant_file_access(self, ids: List[str]) -> Dict :
        """Get files grant token"""
        
        access_token = self._http_client.post('api/file-manager/grant/files', json={ "ids": ids })
        
        log_raise_for_status(access_token)
        
        return get_response_json(access_token)
    

    def upload_file(self, batch_id: str, file : BinaryIO, folder) -> Dict :
        """Upload file without dataset"""
        
        files = {'file': file }

        uploaded = self._http_client.post('api/file-manager/files', files=files, params={ "skipTaskCreation" : "true" }, data={ "path": folder, "batchId": batch_id })
        
        log_raise_for_status(uploaded)
        
        return get_response_json(uploaded)