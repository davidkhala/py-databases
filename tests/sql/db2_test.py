import unittest

from davidkhala.data.base.db2.dba import DBA
from davidkhala.data.base.db2.testcontainers import Container
from davidkhala.data.base.sql import SQL


class DB2TestCase(unittest.TestCase):
    def setUp(self):
        self.container = Container()
        self.container.start()
    def test_connect(self):
        sql = SQL(self.container.get_connection_url())
        sql.connect()
        dba = DBA(sql)
        self.assertEqual('DB2 v12.1.4.0', dba.version)

    def tearDown(self):
        self.container.stop()


if __name__ == '__main__':
    unittest.main()
