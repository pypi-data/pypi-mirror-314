from abc import ABC
from isahitlab.core.http.http_client import HttpClient


class BaseApi(ABC):
    """Base class for all API"""
    
    http_client: HttpClient # instantianted in the isahitlab client child class

    def __init__(self, http_client: HttpClient) -> None:
        """Initialize Base Api Class."""
        self._http_client = http_client