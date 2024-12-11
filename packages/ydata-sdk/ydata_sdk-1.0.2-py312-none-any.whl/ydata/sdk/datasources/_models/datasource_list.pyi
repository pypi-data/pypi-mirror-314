class DataSourceList(list):
    class ListItem:
        uid: str
        name: str
        datatype: str
        creation_date: str
        status: str
        connector_uid: str
        def __init__(self, **_) -> None: ...
