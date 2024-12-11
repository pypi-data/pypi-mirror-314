from .connector import Connector
from typing import Optional
from ydata.sdk.connectors._models.schema import Schema

class RDBMSConnector(Connector):
    db_schema: Optional[Schema]
