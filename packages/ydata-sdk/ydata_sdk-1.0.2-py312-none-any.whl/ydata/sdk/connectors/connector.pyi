from pandas import DataFrame as pdDataFrame
from pathlib import Path
from typing import Dict, Optional, Union
from ydata.sdk.common.client import Client
from ydata.sdk.common.types import Project, UID
from ydata.sdk.connectors._models.connector_list import ConnectorsList
from ydata.sdk.connectors._models.connector_type import ConnectorType
from ydata.sdk.connectors._models.credentials.credentials import Credentials
from ydata.sdk.connectors._models.schema import Schema
from ydata.sdk.utils.model_mixin import ModelFactoryMixin

class Connector(ModelFactoryMixin):
    def __init__(self, connector_type: Union[ConnectorType, str, None] = ..., credentials: Optional[Dict] = ..., name: Optional[str] = ..., project: Optional[Project] = ..., client: Optional[Client] = ...) -> None: ...
    @property
    def uid(self) -> UID: ...
    @property
    def name(self) -> str: ...
    @property
    def type(self) -> ConnectorType: ...
    @property
    def project(self) -> Project: ...
    @staticmethod
    def get(uid: UID, project: Optional[Project] = ..., client: Optional[Client] = ...) -> _T: ...
    @staticmethod
    def create(connector_type: Union[ConnectorType, str], credentials: Union[str, Path, Dict, Credentials], name: Optional[str] = ..., project: Optional[Project] = ..., client: Optional[Client] = ...) -> _T: ...
    @staticmethod
    def list(project: Optional[Project] = ..., client: Optional[Client] = ...) -> ConnectorsList: ...

class RDBMSConnector(Connector):
    @property
    def schema(self) -> Optional[Schema]: ...

class LocalConnector(Connector):
    @staticmethod
    def create(source: Union[pdDataFrame, str, Path], connector_type: Union[ConnectorType, str] = ..., name: Optional[str] = ..., project: Optional[Project] = ..., client: Optional[Client] = ...) -> LocalConnector: ...
