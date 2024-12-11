from typing import Optional
from ydata.core.enum import StringEnum
from ydata.sdk.common.model import BaseModel
from ydata.sdk.common.status import GenericStateErrorStatus

class PrepareState(StringEnum):
    PREPARING: str
    DISCOVERING: str
    FINISHED: str
    FAILED: str

class TrainingState(StringEnum):
    PREPARING: str
    RUNNING: str
    FINISHED: str
    FAILED: str

class ReportState(StringEnum):
    PREPARING: str
    GENERATING: str
    AVAILABLE: str
    FAILED: str
PrepareStatus = GenericStateErrorStatus[PrepareState]
TrainingStatus = GenericStateErrorStatus[TrainingState]
ReportStatus = GenericStateErrorStatus[ReportState]

class Status(BaseModel):
    class State(StringEnum):
        NOT_INITIALIZED: str
        UNKNOWN: str
        PREPARE: str
        TRAIN: str
        REPORT: str
        READY: str
    state: Optional[State]
    prepare: Optional[PrepareStatus]
    training: Optional[TrainingStatus]
    report: Optional[ReportStatus]
    @staticmethod
    def not_initialized() -> Status: ...
    @staticmethod
    def unknown() -> Status: ...
