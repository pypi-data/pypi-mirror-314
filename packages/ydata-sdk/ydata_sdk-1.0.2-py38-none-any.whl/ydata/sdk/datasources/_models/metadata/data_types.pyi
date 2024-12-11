from ydata.core.enum import StringEnum

class DataType(StringEnum):
    NUMERICAL: str
    CATEGORICAL: str
    DATE: str
    LONGTEXT: str
    STR: str

class VariableType(StringEnum):
    INT: str
    FLOAT: str
    STR: str
    BOOL: str
    DATETIME: str
    DATE: str
