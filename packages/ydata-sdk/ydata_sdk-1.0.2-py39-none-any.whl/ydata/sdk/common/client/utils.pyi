from _typeshed import Incomplete
from pathlib import Path
from typing import Dict, Optional, Union
from ydata.sdk.common.client.client import Client

CLIENT_INIT_TIMEOUT: Incomplete
WAITING_FOR_CLIENT: bool

def get_client(client_or_creds: Optional[Union[Client, Dict, str, Path]] = ..., set_as_global: bool = ..., wait_for_auth: bool = ...) -> Client: ...
def init_client(func): ...
