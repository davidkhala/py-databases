from time import sleep

from sqlalchemy.exc import InterfaceError, OperationalError

from davidkhala.data.base.sql import SQL


class ConnectString:
    @staticmethod
    def build(
            domain: str,
            *,
            port=1433,
            username: str | None, password: str | None,
            dbname: str | None = None,
            insecure=False,
            queries: dict | None = None,
    ) -> str:
        queries = queries or {}
        queries["driver"] = "ODBC+Driver+18+for+SQL+Server"
        queries["TrustServerCertificate"] = "yes" if insecure else "no"

        return SQL.connect_string(
            "mssql", domain,
            port=port,
            driver="pyodbc",
            username=username, password=password,
            name=dbname,
            queries=queries,
        )

    @staticmethod
    def decorate(connect_string: str, *, insecure=False) -> str:
        return (f"{connect_string}"
                f"?driver=ODBC+Driver+18+for+SQL+Server"
                f"{'&TrustServerCertificate=yes' if insecure else ''}"
                )


class Client(SQL):
    def connect(self) -> bool:
        try:
            self.connection = self.client.connect()
            return True
        except InterfaceError as e:
            if e.orig.args[0] == 'IM002':
                print(e.orig.args[1])
            else:
                raise
        return False


class ColdClient(Client):
    def connect(self) -> bool:
        try:
            return super().connect()
        except OperationalError as e:
            if e.orig.args[0] == '08001':
                print(e.orig.args[1])
                sleep(10)
                return self.connect()
            else:
                raise
