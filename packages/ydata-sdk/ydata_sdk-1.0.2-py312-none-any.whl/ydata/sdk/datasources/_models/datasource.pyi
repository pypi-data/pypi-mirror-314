from typing import Optional
from ydata.sdk.common.types import UID
from ydata.sdk.datasources._models.datatype import DataSourceType
from ydata.sdk.datasources._models.metadata.metadata import Metadata
from ydata.sdk.datasources._models.status import Status

class DataSource:
    uid: Optional[UID]
    author: Optional[str]
    name: Optional[str]
    datatype: Optional[DataSourceType]
    metadata: Optional[Metadata]
    status: Optional[Status]
    def __post_init__(self) -> None: ...
    def to_payload(self): ...
