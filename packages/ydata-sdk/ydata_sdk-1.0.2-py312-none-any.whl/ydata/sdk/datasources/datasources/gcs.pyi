from typing import Optional, Union
from ydata.sdk.common.client import Client
from ydata.sdk.connectors.connector import Connector
from ydata.sdk.datasources._models.datatype import DataSourceType
from ydata.sdk.datasources._models.filetype import FileType
from ydata.sdk.datasources.datasource import DataSource

class GCSDataSource(DataSource):
    def __init__(self, connector: Connector, path: str, datatype: Optional[Union[DataSourceType, str]] = ..., filetype: Union[FileType, str] = ..., separator: str = ..., name: Optional[str] = ..., wait_for_metadata: bool = ..., client: Optional[Client] = ...) -> None: ...
