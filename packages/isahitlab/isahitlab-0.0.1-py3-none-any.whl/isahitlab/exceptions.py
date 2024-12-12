import json

class AuthenticationFailed(Exception):
    def __init__(self, access_id, secret_key) -> None:
        if access_id is None or secret_key is None:
            super().__init__("You need to provide an access id and its associated secret key to connect.")
        else:
            super().__init__("Connection to isahit lab failed. Check your access id and secret key.")

class ApiBadRequest(Exception):
    def __init__(self, message) -> None:
        try:
            message = json.dumps(json.loads(message), indent=2)
        except:
            # IGNORE
            pass
        super().__init__(message)

class ApiForbidden(Exception):
    def __init__(self, message) -> None:
        try:
            message = json.dumps(json.loads(message), indent=2)
        except:
            # IGNORE
            pass
        super().__init__(message)

class InternalServerError(Exception):
    def __init__(self, message) -> None:
        try:
            message = json.dumps(json.loads(message), indent=2)
        except:
            # IGNORE
            pass
        super().__init__(message)