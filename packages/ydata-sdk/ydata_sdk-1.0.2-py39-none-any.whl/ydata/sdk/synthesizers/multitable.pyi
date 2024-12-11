from typing import Dict, List, Optional, Union
from ydata.datascience.common import PrivacyLevel
from ydata.sdk.common.client import Client
from ydata.sdk.common.types import Project, UID
from ydata.sdk.connectors.connector import Connector
from ydata.sdk.datasources import DataSource
from ydata.sdk.datasources._models.datatype import DataSourceType
from ydata.sdk.datasources._models.metadata.data_types import DataType
from ydata.sdk.synthesizers.synthesizer import BaseSynthesizer

class MultiTableSynthesizer(BaseSynthesizer):
    def __init__(self, write_connector: Union[Connector, UID], uid: Optional[UID] = ..., name: Optional[str] = ..., project: Optional[Project] = ..., client: Optional[Client] = ...) -> None: ...
    def fit(self, X: DataSource, privacy_level: PrivacyLevel = ..., datatype: Optional[Union[DataSourceType, str]] = ..., sortbykey: Optional[Union[str, List[str]]] = ..., entities: Optional[Union[str, List[str]]] = ..., generate_cols: Optional[List[str]] = ..., exclude_cols: Optional[List[str]] = ..., dtypes: Optional[Dict[str, Union[str, DataType]]] = ..., target: Optional[str] = ..., anonymize: Optional[dict] = ..., condition_on: Optional[List[str]] = ...) -> None: ...
    def sample(self, frac: Union[int, float] = ..., write_connector: Optional[Union[Connector, UID]] = ...) -> None: ...
