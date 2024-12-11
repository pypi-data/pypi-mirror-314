from typing import Dict, List, Union
from ydata.sdk.common.model import BaseModel
from ydata.sdk.datasources._models.metadata.data_types import DataType

class DataSourceAttrs(BaseModel):
    sortbykey: Union[str, List[str]]
    entities: Union[str, List[str]]
    generate_cols: List[str]
    exclude_cols: List[str]
    dtypes: Dict[str, Union[str, DataType]]
    def __init__(self, **fields) -> None: ...
