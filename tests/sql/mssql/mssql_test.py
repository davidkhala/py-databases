import unittest

import sqlalchemy
from sqlalchemy import Engine
from sqlalchemy.engine.create import create_engine

from davidkhala.data.base.mssql import Client
from davidkhala.data.base.mssql.dba import DBA
from davidkhala.data.base.sql import SQL

USERNAME = "PROD_DataStage_SA_2606"
PASSWORD = ""
HOST = "10.10.20.209"
PORT = 1433
DATABASE = "maximdb"
PROXY_HOST = "130.198.21.240"
PROXY_PORT = 29130
from davidkhala.data.base.mssql.testcontainers import Container

class TestContainerWithTDSTestCase(unittest.TestCase):
    def setUp(self):
        self.container = Container(dialect="mssql+pytds")
        self.container.start()
    def test_smoke(self):
        url = self.container.get_connection_url()
        self.assertTrue(url.startswith("mssql+pytds://SA:"))
        self.assertTrue(url.endswith('tempdb'))
    def test_connect(self):
        engine: Engine = create_engine(
            self.container.get_connection_url(),
        )
        with engine.begin() as connection:
            result = connection.execute(sqlalchemy.text("SELECT SERVERPROPERTY('ProductVersion')"))
            self.assertEqual("17.0.4065.4", result.scalar())
    def tearDown(self):
        self.container.stop()

class TestContainerWithODBCTestCase(unittest.TestCase):
    def setUp(self):
        self.container = Container(dialect="mssql+pytds")
        self.container.start()

    def tearDown(self):
        self.container.stop()

class MssqlTestCase(unittest.TestCase):
    def setUp(self):
        connection_string = SQL.connect_string(
            "mssql",
            HOST,
            port=PORT,
            username=USERNAME,
            password=PASSWORD,
            name=DATABASE,
        )
        self.client = Client(
            connection_string,
            proxy={"host": PROXY_HOST, "port": PROXY_PORT},
        )

    def test_connect_and_inspect(self):
        with self.client.client.connect() as connection:
            self.client.connection = connection
            dba = DBA(self.client)

            self.assertIn(DATABASE, dba.databases)

            schemas = dba.schemas()
            self.assertTrue(schemas)

            schema_name = "dbo" if "dbo" in schemas else schemas[0]
            tables = dba.tables(schema_name)
            self.assertIsInstance(tables, list)

            if tables:
                columns = dba.table_schema(tables[0], schema_name)
                self.assertIsInstance(columns, list)
                if columns:
                    self.assertIn("name", columns[0])


if __name__ == '__main__':
    unittest.main()
