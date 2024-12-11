class SynthesizersList(list):
    class ListItem:
        id: str
        name: str
        creation_date: str
        status: str
        def __init__(self, **_) -> None: ...
