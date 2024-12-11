from typing import Any, Dict, Optional, Union

class ConnectorsList(list):
    class ListItem:
        uid: str
        type: str
        name: str
        creation_date: str
        status: str
        datasources_count: Union[int, str]
    def get_by_name(self, name: str, default: Optional[Any] = ...) -> Union[Dict, Any]: ...
    def get_by_uid(self, uid: str, default: Optional[Any] = ...) -> Union[Dict, Any]: ...
