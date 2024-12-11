from enum import Enum

class ConnectorType(str, Enum):
    AWS_S3: str
    AZURE_BLOB: str
    GCS: str
    FILE: str
    MYSQL: str
    AZURE_SQL: str
    BIGQUERY: str
    SNOWFLAKE: str
    @property
    def is_rdbms(self) -> bool: ...
