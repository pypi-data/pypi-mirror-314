from ydata.sdk.common.model import BaseModel
from ydata.sdk.datasources._models.metadata.data_types import DataType, VariableType

class Column(BaseModel):
    name: str
    datatype: DataType
    vartype: VariableType
    class Config:
        use_enum_values: bool
