from typing import Any

from davidkhala.utils.protocol import SupportsClose


class Connectable:
    def __init__(self):
        self.client: Any
        self.connection: SupportsClose | None = None

    def connect(self) -> bool: ...

    def close(self):
        self.connection.close()

    def __enter__(self):
        assert self.connect(), f"{self.__class__.__name__}::connect() failed"
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
