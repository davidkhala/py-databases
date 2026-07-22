from __future__ import annotations

from enum import Enum
from typing import Any, TypedDict

import socks

from davidkhala.data.base.sql import SQL


class ProxyConfigRequired(TypedDict):
    host: str
    port: int


class ProxyType(Enum):
    HTTP = socks.HTTP
    SOCKS5 = socks.SOCKS5


class ProxyConfig(ProxyConfigRequired, total=False):
    type: int | ProxyType
    username: str
    password: str
    rdns: bool


class Client(SQL):
    def __init__(
            self,
            *,
            domain: str,
            username: str,
            password: str,
            proxy: ProxyConfig | None = None,
            port: int = 1433,
            name: str = "",
            connect_kwargs: dict[str, Any] | None = None,
            **engine_kwargs,
    ):
        self.domain = domain
        self.port = port
        self.username = username
        self.password = password
        self.name = name
        self.proxy = proxy
        self.connect_kwargs = dict(connect_kwargs or {})

        if proxy:
            super().__init__(
                "mssql+pytds://",
                creator=self._create_proxy_connection,
                **engine_kwargs,
            )
        else:
            super().__init__(
                SQL.connect_string(
                    "mssql", domain,
                    driver="pytds",
                    port=port,
                    username=username,
                    password=password,
                    name=name,
                ),
                **engine_kwargs,
            )

    def _create_proxy_connection(self):
        import pytds

        proxy = self.proxy
        assert proxy is not None

        sock = socks.socksocket()
        try:
            sock.set_proxy(
                proxy.get("type", socks.SOCKS5),
                proxy["host"],
                proxy["port"],
                username=proxy.get("username"),
                password=proxy.get("password"),
                rdns=proxy.get("rdns"),
            )
            sock.connect((self.domain, self.port))
            return pytds.connect(
                sock=sock,
                server=self.domain,
                port=self.port,
                database=self.name or None,
                user=self.username,
                password=self.password,
                **self.connect_kwargs,
            )
        except Exception:
            sock.close()
            raise
