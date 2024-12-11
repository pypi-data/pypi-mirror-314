from _typeshed import Incomplete

class SingletonClient(type):
    GLOBAL_CLIENT: Incomplete
    def __call__(cls, set_as_global: bool = ..., *args, **kwargs): ...
