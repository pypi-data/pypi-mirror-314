from typing import Optional, Union
from ydata.sdk.common.client import Client
from ydata.sdk.common.types import Project
from ydata.sdk.connectors.connector import LocalConnector
from ydata.sdk.datasources._models.datatype import DataSourceType
from ydata.sdk.datasources._models.filetype import FileType
from ydata.sdk.datasources.datasource import DataSource

class LocalDataSource(DataSource):
    def __init__(self, connector: LocalConnector, name: Optional[str] = ..., project: Optional[Project] = ..., datatype: Optional[Union[DataSourceType, str]] = ..., filetype: Union[FileType, str] = ..., separator: str = ..., wait_for_metadata: bool = ..., client: Optional[Client] = ...) -> None: ...
