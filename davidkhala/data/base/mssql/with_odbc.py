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
