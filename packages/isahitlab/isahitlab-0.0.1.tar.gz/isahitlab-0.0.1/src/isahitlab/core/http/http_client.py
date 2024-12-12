"""HTTP client."""

from urllib.parse import urljoin
import requests
import json
import datetime
import logging
from isahitlab.core.http.auth import Credentials
from isahitlab.exceptions import AuthenticationFailed, ApiBadRequest
from isahitlab.core.constants import AUTH_REFRESHING_SPAN

class HttpClient:
    """HTTP client.
    """

    def __init__(self, endpoint: str, credentials: Credentials, auth_route = "api/user-manager/auth/login", defer_auth: bool = True) -> None:
        """Initialize the HTTP client."""

        logging.basicConfig()
        self.logger = logging.getLogger('isahitlab.http')
        self.logger.setLevel(logging.INFO)

        self._isahit_lab_endpoint = endpoint

        self._http_client = requests.Session()
        self._http_client_with_auth = requests.Session()

        self._credentials = credentials

        self._auth_expires_at = None

        self._auth_route = auth_route

        if not defer_auth:
            self._auth()
        # self._auth_headers = {"Authorization": f"X-API-Key: {api_key}"}
        # self._http_client_with_auth.headers.update(self._auth_headers)

    def _auth(self):
        """Get token from credentials"""

        res = self.post(urljoin(self._isahit_lab_endpoint, self._auth_route), data=self._credentials)

        if res.status_code == 401:
            raise AuthenticationFailed(self._credentials['access_id'], self._credentials["secret_key"])
        elif res.status_code == 400:
            raise ApiBadRequest(res.content)
        elif res.status_code != 201:
            raise Exception(res.content)
        
        token = json.loads(res.content)

        access_token = token['access_token']
        expires_in = token['expires_in'] #timeout in seconds

        expires_at = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
        
        self._auth_expires_at = expires_at
        self._auth_headers = {"Authorization": f"Bearer {access_token}"}
        

    def _should_authenticate(self):
        """Check for token expiration"""
        
        if self._auth_expires_at and (datetime.datetime.now() +  datetime.timedelta(seconds=AUTH_REFRESHING_SPAN) < self._auth_expires_at):
            return False

        return True

    def _send_request(self, method: str, url: str, **kwargs) -> requests.Response:

        """Send a request to the given URL."""
        if not url.startswith('http'):
            # Get or refresh token
            if self._should_authenticate():
                self._auth()

            http_client = self._http_client_with_auth
            
            # Add authorization headers
            if kwargs.get("headers") is None:
                kwargs["headers"] = {}
            if "Authorization" not in kwargs["headers"]:
                kwargs["headers"].update(self._auth_headers)

            url = urljoin(self._isahit_lab_endpoint, url)
        else:
            http_client = self._http_client
        
        return http_client.request(method, url, **kwargs)

    def get(self, url: str, **kwargs) -> requests.Response:
        """Send a GET request to the given URL."""
        return self._send_request("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        """Send a POST request to the given URL."""
        return self._send_request("POST", url, **kwargs)

    def head(self, url: str, **kwargs) -> requests.Response:
        """Send a HEAD request to the given URL."""
        return self._send_request("HEAD", url, **kwargs)

    def put(self, url: str, **kwargs) -> requests.Response:
        """Send a PUT request to the given URL."""
        return self._send_request("PUT", url, **kwargs)

    def patch(self, url: str, **kwargs) -> requests.Response:
        """Send a PATCH request to the given URL."""
        return self._send_request("PATCH", url, **kwargs)

    def options(self, url: str, **kwargs) -> requests.Response:
        """Send a OPTIONS request to the given URL."""
        return self._send_request("OPTIONS", url, **kwargs)
