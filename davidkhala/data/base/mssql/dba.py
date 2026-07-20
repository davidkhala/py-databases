from davidkhala.data.base.mssql import Client


class DBA:
    def __init__(self, client: Client):
        self._ = client

    @property
    def databases(self) -> list[str]:
        return self._.list_databases()

    def schemas(self) -> list[str]:
        return self._.list_schemas()

    def tables(self, schema: str = "dbo") -> list[str]:
        return self._.list_tables(schema=schema)

    def table_schema(self, table_name: str, schema: str = "dbo") -> list[dict]:
        return self._.inspect_table_schema(table_name, schema=schema)
