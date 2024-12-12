""" Domain Filter to API params"""
from isahitlab.domain.project import ProjectFilters

def project_filters_mapper(filters: ProjectFilters):
    params = {
        "pagination" : "false" if filters.pagination == False else "true",
        "page" : filters.page,
        "limit" : filters.limit
    }

    if filters.id_in and len(filters.id_in):
        params['ids'] = filters.id_in

    if filters.status_in and len(filters.status_in):
        params['statuses'] = filters.status_in

    if filters.type_in and len(filters.type_in):
        params['types'] = filters.type_in

    if filters.search and len(filters.search):
        params['search'] = filters.search
        
    return params