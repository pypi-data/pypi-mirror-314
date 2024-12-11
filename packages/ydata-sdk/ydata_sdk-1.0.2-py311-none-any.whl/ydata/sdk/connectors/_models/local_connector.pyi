from .connector import Connector
from typing import Optional

class LocalConnector(Connector):
    file: Optional[str]
