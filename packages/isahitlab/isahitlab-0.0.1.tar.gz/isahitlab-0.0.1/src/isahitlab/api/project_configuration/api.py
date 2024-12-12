from typing import Dict
from isahitlab.api.base import BaseApi
from isahitlab.domain.project import ProjectId
from ..helpers import get_response_json, log_raise_for_status

class ProjectConfigurationApi(BaseApi):
    """Project configuration API Calls"""

    def get_project_configuration(self, project_id : ProjectId) -> Dict :
        """Get tasks"""

        project_configuration = self._http_client.get('api/project-configuration-manager/projects/{}/project-configuration'.format(project_id))

        log_raise_for_status(project_configuration)

        return get_response_json(project_configuration)
