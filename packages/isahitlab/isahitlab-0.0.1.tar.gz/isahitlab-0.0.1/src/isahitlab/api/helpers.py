import requests
import json
import logging
from typing import TypedDict, Iterable, Dict, Union
from ..exceptions import ApiBadRequest, AuthenticationFailed, InternalServerError, ApiForbidden
class Paginated(TypedDict):
    """Paginated result"""

    docs: Iterable[Dict]
    totalDocs: int
    limit: int
    totalPages: int
    page: int
    pagingCounter: int
    hasPrevPage: bool
    hasNextPage: bool
    prevPage: Union[int, None]
    nextPage: Union[int, None]


def log_raise_for_status(response: requests.Response) -> None:
    """Log the error message of a requests.Response if it is not ok.

    Args:
        response: a requests.Response
    """
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 401:
            raise AuthenticationFailed()
        elif err.response.status_code == 400:
            raise ApiBadRequest(err.response.content)
        elif err.response.status_code == 403:
            raise ApiForbidden(err.response.content)
        elif err.response.status_code == 500:
            raise InternalServerError(err.response.content)
        else:
            raise


def get_response_json(response: requests.Response) -> dict:
    """Get the json from a requests.Response.

    Args:
        response: a requests.Response
    """
    try:
        return response.json()
    except json.JSONDecodeError:
        logging.exception("An error occurred while decoding the json response")
        return {}