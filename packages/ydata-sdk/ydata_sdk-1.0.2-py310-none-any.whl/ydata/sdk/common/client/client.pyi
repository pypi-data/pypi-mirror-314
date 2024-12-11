from _typeshed import Incomplete
from httpx import Response as Response, codes as http_codes
from httpx._types import RequestContent as RequestContent
from typing import Dict, Optional, Union
from ydata.sdk.common.client.singleton import SingletonClient
from ydata.sdk.common.types import Project

codes = http_codes
HELP_TEXT: Incomplete

class Client(metaclass=SingletonClient):
    codes = codes
    DEFAULT_PROJECT: Optional[Project]
    def __init__(self, credentials: Optional[Union[str, Dict]] = ..., project: Optional[Project] = ..., set_as_global: bool = ...) -> None: ...
    @property
    def project(self) -> Project: ...
    def post(self, endpoint: str, content: Optional[RequestContent] = ..., data: Optional[Dict] = ..., json: Optional[Dict] = ..., project: Optional[Project] = ..., files: Optional[Dict] = ..., raise_for_status: bool = ...) -> Response: ...
    def patch(self, endpoint: str, content: Optional[RequestContent] = ..., data: Optional[Dict] = ..., json: Optional[Dict] = ..., project: Optional[Project] = ..., files: Optional[Dict] = ..., raise_for_status: bool = ...) -> Response: ...
    def get(self, endpoint: str, params: Optional[Dict] = ..., project: Optional[Project] = ..., cookies: Optional[Dict] = ..., raise_for_status: bool = ...) -> Response: ...
    def get_static_file(self, endpoint: str, project: Optional[Project] = ..., raise_for_status: bool = ...) -> Response: ...
