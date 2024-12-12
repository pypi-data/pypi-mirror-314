from typing import Dict, Any
from isahitlab.api.base import BaseApi
from ..helpers import get_response_json, log_raise_for_status

class DataApi(BaseApi):
    """Data API Calls"""

    def import_data(self, batch_id: str, name : str, body: Dict[str, Any]) -> Dict :
        """Get files grant token"""
        
        data = self._http_client.post('api/data-manager/import-data/json', 
                                      params= {
                                        "skipTaskCreation" : "true",
                                        "grantAccess" : "true"

                                    }, 
                                    json={ 
                                        "batchId": batch_id,
                                        "name" : name,
                                        "body" : body
                                    }
        )
        
        log_raise_for_status(data)
        
        return get_response_json(data)
    