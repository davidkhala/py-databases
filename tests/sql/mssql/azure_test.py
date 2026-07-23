import os
import unittest
from time import sleep

from davidkhala.data.base.mssql.with_odbc import ConnectString
from davidkhala.data.base.sql import SQL


class AzureTestCase(unittest.TestCase):
    def setUp(self):
        domain = 'sql-server-hk.database.windows.net'
        name = 'mssql'
        username = 'CloudSA7b5eda98'
        password = os.environ.get("MSSQL_PASSWORD") or 'Kd5zbER2aJ3SnC'
        queries = {
            "Encrypt": "yes",
        }
        self.client = SQL(ConnectString.build(
            domain,
            username=username,
            password=password,
            dbname=name,
            queries=queries
        ))

    def test_connect(self):
        warm = self.client.connect()
        if not warm:
            sleep(60)
            self.assertTrue(self.client.connect())
