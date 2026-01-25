from davidkhala.data.base import Connectable
from davidkhala.utils.syntax.interface import Delegate
from duckdb import DuckDBPyConnection, connect


class DB(Connectable, Delegate):
    def connect(self) -> bool:
        self.client: DuckDBPyConnection = connect()
        return True

    def close(self):
        self.client.close()
