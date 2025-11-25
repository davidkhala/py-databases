from typing import Dict, Any

from davidkhala.data.base.common import Connectable
from sqlalchemy import create_engine, text, Engine, CursorResult


class SQL(Connectable):
    def __init__(self, connection_string: str):
        super().__init__()
        self.connection = None
        self.connection_string = connection_string
        self.client: Engine = create_engine(connection_string)

    def connect(self):
        self.connection = self.client.connect()

    def disconnect(self):
        self.connection.close()

    def query(self,
              template: str,
              values: Dict[str, Any]|None = None,
              request_options: Dict[str, Any]|None = None
              ) -> CursorResult[Any]:
        return self.connection.execute(text(template), values, execution_options=request_options)
    @staticmethod
    def rows_to_dicts(result:CursorResult): return result.mappings().all()
