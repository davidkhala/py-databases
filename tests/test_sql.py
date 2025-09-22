import unittest

from testcontainers.mysql import MySqlContainer

from davidkhala.mysql import Mysql


class MysqlTestCase(unittest.TestCase):
    def setUp(self):
        self.container = MySqlContainer(port=3406) # avoid github runner port conflict
        self.container.start()
    def test_connect(self):
        mysql = Mysql(self.container.get_connection_url())
        mysql.connect()
        mysql.disconnect()

    def tearDown(self):
        self.container.stop()


if __name__ == '__main__':
    unittest.main()
