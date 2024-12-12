from typing import Dict, Generator
import time
from isahitlab.api.base import BaseApi
from isahitlab.domain.project import ProjectFilters
from ..helpers import get_response_json, log_raise_for_status, Paginated
from .mappers import project_filters_mapper

class ProjectApi(BaseApi):
    """Project API Calls"""

    def get_all_projects(self, filters: ProjectFilters) -> Generator[tuple[Dict, int, int], None, None] :
        """Get tasks"""

        page = 1
        limit = 10

        filters.pagination = True
        filters.limit = limit

        while True:
            filters.page = page

            paginated: Paginated = self._get_project_page(filters)
            docs = paginated['docs']
            page = paginated['nextPage']

            # Count already loaded
            totalDocs = paginated['totalDocs']
            loaded = (paginated['page'] - 1) * paginated['limit'] + len(docs)

            yield (docs, loaded, totalDocs)

            if not paginated['hasNextPage']:
                break

            time.sleep(0.5)



    
    def _get_project_page(self, filters: ProjectFilters) -> Paginated :
        """Get projects page"""
        
        tasks = self._http_client.get('api/project-manager/projects', params=project_filters_mapper(filters))
        
        log_raise_for_status(tasks)
        
        return get_response_json(tasks)