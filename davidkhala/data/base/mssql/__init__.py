import socket
from contextlib import contextmanager
from typing import Any, Iterator, Mapping

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine

from davidkhala.data.base.__init__ import Connectable
from davidkhala.data.base.sql import SQL

DEFAULT_DRIVER = "pyodbc"
PROXY_CAPABLE_DRIVERS = "pytds"


class Client(SQL):
    def __init__(
        self,
        connection_string: str,
        *,
        driver: str | None = None,
        proxy: Mapping[str, Any] | None = None,
        **engine_kwargs,
    ):
        Connectable.__init__(self)
        self.proxy = dict(proxy) if proxy else None
        parts = SQL.parse(connection_string)
        chosen_driver = driver or (
            PROXY_CAPABLE_DRIVERS
            if self.proxy is not None
            else DEFAULT_DRIVER
        )
        self.connection_string = SQL.connect_string(
            "mssql",
            parts["domain"],
            driver=chosen_driver,
            port=parts["port"],
            username=parts["username"],
            password=parts["password"],
            name=parts["name"],
            queries={
                key: value
                for key, value in parts["options"].items()
                if chosen_driver == "pyodbc" or key != "driver"
            },
        )

        current_driver = SQL.parse(self.connection_string)["driver"]
        if self.proxy and current_driver != PROXY_CAPABLE_DRIVERS:
            raise ValueError(
                "Proxy support currently requires the pytds driver."
            )

        options = dict(engine_kwargs)
        if self.proxy:
            options["creator"] = self._create_proxy_connection

        self.client: Engine = create_engine(self.connection_string, **options)

    @staticmethod
    def _coerce_option_value(value: str) -> Any:
        lowered = value.lower()
        if lowered == "true":
            return True
        if lowered == "false":
            return False
        if value.isdigit():
            return int(value)
        return value

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

        parts = SQL.parse(self.connection_string)
        options = {
            key: self._coerce_option_value(value)
            for key, value in parts["options"].items()
        }
        with self._proxy_context():
            return pytds.connect(
                server=parts["domain"],
                port=parts["port"] or 1433,
                database=parts["name"] or None,
                user=parts["username"],
                password=parts["password"],
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


class Mssql(Client):
    pass
