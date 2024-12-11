from .model import BaseModel
from typing import Generic, Optional, TypeVar

T = TypeVar('T')

class GenericStateErrorStatus(BaseModel, Generic[T]):
    state: Optional[T]
    class Config:
        use_enum_values: bool
