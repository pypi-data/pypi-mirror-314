from typing import List, Optional
from ydata.sdk.common.model import BaseModel
from ydata.sdk.datasources._models.metadata.column import Column
from ydata.sdk.datasources._models.metadata.warnings import MetadataWarning

class Cardinality(BaseModel):
    column: str
    value: int

class LongTextStatistics(BaseModel):
    average_number_of_characters: int
    average_number_of_words: int

class Metadata(BaseModel):
    cardinality: Optional[List[Cardinality]]
    columns: List[Column]
    duplicate_rows: int
    long_text_statistics: Optional[LongTextStatistics]
    memory: str
    missing_cells: int
    number_of_rows: int
    warnings: Optional[List[MetadataWarning]]
