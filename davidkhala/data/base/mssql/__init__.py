import socket
from contextlib import contextmanager
from typing import Any, Iterator, TypedDict

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine

from davidkhala.data.base.sql import SQL

DEFAULT_DRIVER = "pyodbc"
PROXY_CAPABLE_DRIVERS = "pytds"


class ProxyConfigRequired(TypedDict):
    host: str
    port: int


class ProxyConfig(ProxyConfigRequired, total=False):
    type: str
    username: str
    password: str
    rdns: bool


class Client(SQL):
    def __init__(
            self,
            *,
            connection_string: str | None = None,
            domain: str,
            username: str, password: str,
            port: str | int = 1433, name: str = "",
            queries: dict | None = None,
            proxy: ProxyConfig | None = None,
            **engine_kwargs,
    ):
        queries = dict(queries or {})
        self.domain = domain
        self.port = port
        self.username = username
        self.password = password
        self.name = name
        self.queries = queries
        self.connection = None
        if proxy:
            self.proxy = proxy
            queries.pop("driver", None)
            engine_kwargs["creator"] = self._create_proxy_connection
            self.connection_string = None
            self.client = create_engine(
                "mssql+pytds://", **engine_kwargs
            )
        else:
            self.proxy = None
            driver = DEFAULT_DRIVER
            queries["driver"] = "ODBC+Driver+18+for+SQL+Server"
            connection_string = SQL.connect_string(
                "mssql", domain,
                port=port,
                driver=driver,
                username=username, password=password,
                name=name,
                queries=queries,
            )
            super().__init__(connection_string)

            self.client: Engine = create_engine(
                self.connection_string, **engine_kwargs
            )

    @staticmethod
    def _coerce_option_value(value: str) -> Any:
        lowered = value.lower()
        if lowered == "true":
            return True
        if lowered == "false":
            return False
        return int(value) if value.isdigit() else value

    @contextmanager
    def _proxy_context(self) -> Iterator[None]:
        if not self.proxy:
            yield
            return

        import socks

        proxy_type_name = str(self.proxy.get("type", "SOCKS5")).upper()
        proxy_type = getattr(socks, proxy_type_name, None)
        if proxy_type is None:
            raise ValueError(f"Unsupported proxy type: {proxy_type_name}")

        original_socket = socket.socket
        socks.set_default_proxy(
            proxy_type,
            self.proxy["host"],
            int(self.proxy["port"]),
            username=self.proxy.get("username"),
            password=self.proxy.get("password"),
            rdns=bool(self.proxy.get("rdns", True)),
        )
        socket.socket = socks.socksocket
        try:
            yield
        finally:
            socket.socket = original_socket
            socks.set_default_proxy()

    def _create_proxy_connection(self):
        import pytds

        options = {
            key: self._coerce_option_value(value)
            for key, value in self.queries.items()
        }
        with self._proxy_context():
            return pytds.connect(
                server=self.domain,
                port=self.port or 1433,
                database=self.name or None,
                user=self.username,
                password=self.password,
                **options,
            )

    def _inspectable(self):
        return self.connection if self.connection is not None else self.client

    def inspector(self):
        return inspect(self._inspectable())

    def list_databases(self) -> list[str]:
        if self.connection is not None:
            result = self.query("SELECT name FROM sys.databases ORDER BY name")
            return result.scalars().all()

        with self.client.connect() as connection:
            result = connection.execute(
                text("SELECT name FROM sys.databases ORDER BY name")
            )
            return result.scalars().all()

    def list_schemas(self) -> list[str]:
        return self.inspector().get_schema_names()

    def list_tables(self, schema: str = "dbo") -> list[str]:
        return self.inspector().get_table_names(schema=schema)

    def inspect_table_schema(
            self, table_name: str, schema: str = "dbo"
    ) -> list[dict[str, Any]]:
        columns = self.inspector().get_columns(table_name, schema=schema)
        return [
            {
                "schema": schema,
                "table": table_name,
                "name": column["name"],
                "type": str(column["type"]),
                "nullable": column.get("nullable"),
                "default": column.get("default"),
                "comment": column.get("comment"),
                "identity": column.get("identity"),
            }
            for column in columns
        ]
