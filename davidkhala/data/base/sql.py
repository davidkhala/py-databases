from typing import Dict, Any
from typing import Union
from urllib.parse import urlparse, parse_qs

from sqlalchemy import create_engine, text, Engine, CursorResult

from davidkhala.data.base.common import Connectable


class SQL(Connectable):
    def __init__(self, connection_string: str):
        super().__init__()
        self.connection = None
        self.connection_string = connection_string
        self.client: Engine = create_engine(connection_string)

    def connect(self):
        self.connection = self.client.connect()

    def query(self,
              template: str,
              values: Dict[str, Any]|None = None,
              request_options: Dict[str, Any]|None = None
              ) -> CursorResult[Any]:
        return self.connection.execute(text(template), values, execution_options=request_options)
    @staticmethod
    def rows_to_dicts(result:CursorResult): return result.mappings().all()

    @staticmethod
    def connect_string(
            dialect: str, domain: str,
            *,
            driver: str | None = None,
            port: Union[str, int] | None,
            username: str | None,
            password: str | None,
            name: str | None = None,
            queries: dict | None = None
    ):

        auth = ''
        if username:
            auth += username
            if password:
                auth += f':{password}'
            auth += '@'

        base = f"{dialect}{'+' + driver if driver else ''}://{auth}{domain}{':' + str(port) if port else ''}{'/' + name if name else ''}"

        if queries:
            query_string = '&'.join(f"{key}={value}" for key, value in queries.items())
            return f"{base}?{query_string}"
        else:
            return base

    @staticmethod
    def parse(connection_string: str):
        o = urlparse(connection_string)

        domain = o.hostname
        port = o.port

        if '+' in o.scheme:
            dialect, driver = o.scheme.split('+', 1)
        else:
            dialect = o.scheme
            driver = None
        username = o.username
        password = o.password

        name = o.path.lstrip('/')

        # extract params
        options = {k: v[0] for k, v in parse_qs(o.query).items()}

        return {
            "dialect": dialect,
            "driver": driver,
            "username": username,
            "password": password,
            "domain": domain,
            "port": port,
            "options": options,
            "name": name
        }