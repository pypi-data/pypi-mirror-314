from typing import Optional, Union
from ydata.sdk.common.client import Client
from ydata.sdk.connectors.connector import Connector
from ydata.sdk.datasources._models.datatype import DataSourceType
from ydata.sdk.datasources.datasource import DataSource

class BigQueryDataSource(DataSource):
    def __init__(self, connector: Connector, query: str, datatype: Optional[Union[DataSourceType, str]] = ..., name: Optional[str] = ..., wait_for_metadata: bool = ..., client: Optional[Client] = ...) -> None: ...
