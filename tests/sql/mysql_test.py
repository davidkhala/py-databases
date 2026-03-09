import os
import socket
import unittest

from davidkhala.data.base.mysql import Mysql
from davidkhala.data.base.mysql.testcontainers import Container as MySqlContainer
from davidkhala.data.base.sql import SQL


class MysqlTestCase(unittest.TestCase):
    def setUp(self):
        self.container = MySqlContainer()
        self.container.start()
        if os.environ.get("CI"):
            host = socket.gethostbyname(socket.gethostname())
            print('host', host)
            self.mysql = Mysql(SQL.connect_string(
                "mysql", host,
                driver="mysqldb", username='test', password='test', name='test',
                port=self.container.get_exposed_port(3306),
            ))
        else:
            connection_string = self.container.get_connection_url()
            print('connection_string', connection_string)
            self.mysql = Mysql(connection_string)

    def test_connect(self):
        self.assertIn(SQL.parse(self.mysql.connection_string)["driver"], [
            "mysqldb", # choice of extra
            'pymysql', # default driver of testcontainers
        ])
        self.mysql.connect()
        self.mysql.close()

    def tearDown(self):
        self.container.stop()


if __name__ == '__main__':
    unittest.main()
