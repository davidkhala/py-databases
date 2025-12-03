from abc import abstractmethod, ABC
from typing import Any


class Connectable(ABC):
    def __init__(self, *args, **kwargs):
        self.connection_string: str
        self.client: Any
        self.connection: Any

    @abstractmethod
    def connect(self):
        ...

    @abstractmethod
    def close(self):
        ...

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
