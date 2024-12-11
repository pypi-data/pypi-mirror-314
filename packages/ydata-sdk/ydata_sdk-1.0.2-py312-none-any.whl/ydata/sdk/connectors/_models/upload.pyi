from typing import Optional
from ydata.sdk.common.model import BaseModel

class Upload(BaseModel):
    uid: str
    chunk_size: int
    file_name: str
    written_bytes: Optional[int]
    total_bytes: Optional[int]
