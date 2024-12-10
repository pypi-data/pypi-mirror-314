import enum

# Client
OVINC_CLIENT_SIGNATURE = "OVINC Client"
OVINC_CLIENT_TIMEOUT = 60

# App Auth
APP_AUTH_HEADER_KEY = "ovinc-app"
APP_AUTH_ID_KEY = "app_code"
APP_AUTH_SECRET_KEY = "app_secret"


# Request
class RequestMethodEnum(enum.Enum):
    GET = "GET"
    POST = "POST"


class ResponseData:
    def __init__(self, result: bool, data: any = None):
        self._result = result
        self._data = data

    @property
    def data(self) -> dict:
        return self._data if self._result else {}
