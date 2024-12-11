from .status import Status
from typing import Optional
from ydata.sdk.common.model import BaseModel

class Synthesizer(BaseModel):
    uid: Optional[str]
    author: Optional[str]
    name: Optional[str]
    status: Optional[Status]
