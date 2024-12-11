from typing import List, Optional
from ydata.sdk.common.model import BaseModel
from ydata.sdk.common.pydantic_utils import to_camel

class BaseConfig(BaseModel.Config):
    alias_generator = to_camel

class TableColumn(BaseModel):
    name: str
    variable_type: str
    primary_key: Optional[bool]
    is_foreign_key: Optional[bool]
    foreign_keys: list
    nullable: bool
    Config = BaseConfig

class Table(BaseModel):
    name: str
    columns: List[TableColumn]
    primary_keys: List[TableColumn]
    foreign_keys: List[TableColumn]
    Config = BaseConfig

class Schema(BaseModel):
    name: str
    tables: Optional[List[Table]]
    Config = BaseConfig
