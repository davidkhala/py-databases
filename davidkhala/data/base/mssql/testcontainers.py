from testcontainers.mssql import SqlServerContainer


class Container(SqlServerContainer):
    def __init__(self, *, name="tempdb", dialect="mssql+pyodbc", **kwargs):
        super().__init__(
            image="mcr.microsoft.com/mssql/server:2025-latest",
            dialect=dialect,
            dbname=name,
            **kwargs)

    @property
    def exposed_port(self):
        return self.get_exposed_port(self.port)
