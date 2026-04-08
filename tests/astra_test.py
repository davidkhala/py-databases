import os
import unittest
from davidkhala.data.base.astra import Client
from davidkhala.data.base.astra.dba import DBA
class BaseTest(unittest.TestCase):
    def setUp(self) -> None:

        token = os.environ.get('TOKEN')
        self._ = Client(token)
        self.endpoint = 'https://a6dbec03-399d-46f6-83f7-93b4e9602c70-us-east-2.apps.astra.datastax.com'
class APITest(BaseTest):
    def test_connect(self):
        self.assertTrue(self._.connect(self.endpoint))

class DBATest(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.dba = DBA(self._)
    def test_connect(self):

        print(self.dba._.list_databases())

if __name__ == '__main__':
    unittest.main()