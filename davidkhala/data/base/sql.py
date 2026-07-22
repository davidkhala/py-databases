from typing import Any
from urllib.parse import urlparse, parse_qs, quote, unquote

from sqlalchemy import create_engine, text, Engine, CursorResult

from davidkhala.data.base.__init__ import Connectable


class SQL(Connectable):
    def __init__(self, connection_string: str, **engine_kwargs):
        super().__init__()
        self.connection_string = connection_string
        self.client: Engine = create_engine(connection_string, **engine_kwargs)

    def connect(self) -> bool:
        try:
            self.connection = self.client.connect()
            return True
        except Exception:
            return False

    def query(self,
              template: str,
              values: dict | None = None,
              request_options: dict | None = None
              ) -> CursorResult[Any]:
        return self.connection.execute(
            text(template),
            values,
            execution_options=request_options,
        )

    @staticmethod
    def rows_to_dicts(result: CursorResult):
        return result.mappings().all()

    @staticmethod
    def connect_string(
            dialect: str, domain: str,
            *,
            driver: str | None = None,
            port: str | int | None,
            username: str | None,
            password: str | None,
            name: str | None = None,
            queries: dict | None = None
    ):

        auth = ''
        if username:
            auth += quote(username, safe='')
            if password:
                auth += f":{quote(password, safe='')}"
            auth += '@'

        scheme = f"{dialect}{'+' + driver if driver else ''}"
        location = (
            f"{auth}{domain}{':' + str(port) if port else ''}"
            f"{'/' + name if name else ''}"
        )
        base = f"{scheme}://{location}"

        if queries:
            query_string = '&'.join(
                f"{key}={value}" for key, value in queries.items()
            )
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
        username = unquote(o.username) if o.username else None
        password = unquote(o.password) if o.password else None

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
    def close(self):
        super().close()
        del self.connection
        self.client.dispose()