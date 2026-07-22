import unittest

import sqlalchemy
from sqlalchemy import Engine
from sqlalchemy.engine.create import create_engine

from davidkhala.data.base.mssql.with_tds import Client

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


from davidkhala.data.base.mssql.with_odbc import ConnectString


class TestContainerWithODBCTestCase(unittest.TestCase):
    def setUp(self):
        self.container = Container()
        self.container.start()

    def test_connect(self):
        engine: Engine = create_engine(
            ConnectString.decorate(self.container.get_connection_url(), insecure=True)
        )
        with engine.begin() as connection:
            result = connection.execute(sqlalchemy.text("SELECT SERVERPROPERTY('ProductVersion')"))
            self.assertEqual("17.0.4065.4", result.scalar())

    def tearDown(self):
        self.container.stop()




class MssqlTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client(
            domain=HOST,
            port=PORT,
            username=USERNAME,
            password=PASSWORD,
            name=DATABASE,
            proxy={"host": PROXY_HOST, "port": PROXY_PORT},
        )

    def test_connect(self):
        self.assertTrue(self.client.connect())

    def tearDown(self):
        self.client.close()


if __name__ == '__main__':
    unittest.main()
