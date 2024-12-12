"""Auth types"""

from typing import TypedDict


class Credentials(TypedDict):
    """API Credentials"""

    access_id: str
    secret_key: str