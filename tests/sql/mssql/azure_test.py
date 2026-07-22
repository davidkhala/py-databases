import os
import unittest

from davidkhala.data.base.mssql.with_odbc import ConnectString
from davidkhala.data.base.sql import SQL


class AzureTestCase(unittest.TestCase):
    def setUp(self):
        domain = 'sql-server-hk.database.windows.net'
        name = 'mssql'
        username = 'CloudSA7b5eda98'
        password = os.environ.get("MSSQL_PASSWORD")
        queries = {
            "Encrypt": "yes",
            "Connection Timeout": 30
        }
        self.client = SQL(ConnectString.build(
            domain,
            username=username,
            password=password,
            dbname=name,
            queries=queries
        ))

    def test_connect(self):
        self.assertTrue(self.client.connect())
