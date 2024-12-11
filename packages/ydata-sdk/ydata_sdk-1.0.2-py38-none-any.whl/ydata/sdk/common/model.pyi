from _typeshed import Incomplete
from pydantic import BaseModel as PydanticBaseModel

class Config:
    allow_population_by_field_name: bool
    extra: Incomplete
    use_enum_values: bool

class BaseModel(PydanticBaseModel):
    Config = Config
