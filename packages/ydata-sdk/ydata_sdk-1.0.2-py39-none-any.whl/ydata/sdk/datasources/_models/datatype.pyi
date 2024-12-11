from ydata.core.enum import StringEnum

class DataSourceType(StringEnum):
    TABULAR: str
    TIMESERIES: str
    MULTITABLE: str
