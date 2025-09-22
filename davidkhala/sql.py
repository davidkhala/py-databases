from typing import Optional, Dict, Any

from sqlalchemy import create_engine, text, Engine

from davidkhala.db import Connectable


class SQL(Connectable):
    def __init__(self, connect_string: str):
        super().__init__()
        self.connect_string = connect_string
        self.client: Engine = create_engine(connect_string)

    def connect(self):
        self.connection = self.client.connect()

    def disconnect(self):
        self.connection.close()

    def query(self, template: str, values: Optional[Dict[str, Any]] = None,
                    request_options: Optional[Dict[str, Any]] = None):
        return self.connection.execute(text(template), values, execution_options=request_options)
