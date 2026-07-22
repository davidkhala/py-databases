import os
import unittest

from davidkhala.data.base.mssql import Client


class AzureTestCase(unittest.TestCase):
    def setUp(self):

        domain ='sql-server-hk.database.windows.net'
        name = 'mssql'
        username = 'CloudSA7b5eda98'
        password = os.environ.get("MSSQL_PASSWORD")
        self.client = Client(
            domain=domain, username=username, password=password,name=name,
        )
    def test_connect(self):
        self.client.connect()