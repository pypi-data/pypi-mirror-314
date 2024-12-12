from abc import ABC
from isahitlab.core.http.http_client import HttpClient


class BaseAction(ABC):
    """Base class for all actions.
    It is used to share the HttpClient between all actions classes.
    It is not meant to be used and instantiated directly.
    """
    
    http_client: HttpClient # instantianted in the isahitlab client child class