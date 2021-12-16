from requests.auth import AuthBase
from requests import PreparedRequest


class BearerAuth(AuthBase):
    def __init__(self, token: str) -> None:
        self.token = token

    def __call__(self, request: PreparedRequest) -> PreparedRequest:
        request.headers["authorization"] = f"Bearer {self.token}"
        return request
