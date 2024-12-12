""" Domain Filter to API params"""
from isahitlab.domain.task import TaskFilters

def task_filters_mapper(filters: TaskFilters):
    params = {
        "pagination" : "false" if filters.pagination == False else "true",
        "page" : filters.page,
        "limit" : filters.limit,
        "projectId" : filters.project_id,
    }

    if filters.batch_id_in and len(filters.batch_id_in):
        params['batchIds'] = filters.batch_id_in

    if filters.status_in and len(filters.status_in):
        params['statuses'] = filters.status_in

    if filters.name_like and len(filters.status_in):
        params['nameKile'] = [filters.name_like]

    if filters.task_id_in and len(filters.task_id_in):
        params['taskIds'] = [filters.task_id_in]

    if filters.name_in and len(filters.name_in):
        params['taskNames'] = [filters.name_in]

    if filters.optional_fields and len(filters.optional_fields):
        params['optionalFields'] = filters.optional_fields

    if filters.created_at_gt and len(filters.created_at_gt):
        if "createdAt" not in params:
            params["createdAt"] = []
        params['createdAt'].append(">{}".format(filters.created_at_gt))

    if filters.created_at_gte and len(filters.created_at_gte):
        if "createdAt" not in params:
            params["createdAt"] = []
        params['createdAt'].append(">={}".format(filters.created_at_gte))

    if filters.created_at_lt and len(filters.created_at_lt):
        if "createdAt" not in params:
            params["createdAt"] = []
        params['createdAt'].append("<{}".format(filters.created_at_lt))

    if filters.created_at_lte and len(filters.created_at_lte):
        if "createdAt" not in params:
            params["createdAt"] = []
        params['createdAt'].append("<={}".format(filters.created_at_lte))

    if filters.updated_at_gt and len(filters.updated_at_gt):
        if "updatedAt" not in params:
            params["updatedAt"] = []
        params['updatedAt'].append(">{}".format(filters.updated_at_gt))

    if filters.updated_at_gte and len(filters.updated_at_gte):
        if "updatedAt" not in params:
            params["updatedAt"] = []
        params['updatedAt'].append(">={}".format(filters.updated_at_gte))

    if filters.updated_at_lt and len(filters.updated_at_lt):
        if "updatedAt" not in params:
            params["updatedAt"] = []
        params['updatedAt'].append("<{}".format(filters.updated_at_lt))

    if filters.updated_at_lte and len(filters.updated_at_lte):
        if "updatedAt" not in params:
            params["updatedAt"] = []
        params['updatedAt'].append("<={}".format(filters.updated_at_lte))

    return params