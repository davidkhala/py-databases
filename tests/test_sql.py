import os
import unittest

from testcontainers.core.wait_strategies import HealthcheckWaitStrategy
from testcontainers.mysql import MySqlContainer

from davidkhala.db import Connectable
from davidkhala.mysql import Mysql


class MysqlTestCase(unittest.TestCase):
    def setUp(self):
        self.container = MySqlContainer()
        self.container.start()
        self.container.waiting_for(HealthcheckWaitStrategy())
        if os.environ.get("CI"):
            import socket
            host = socket.gethostbyname(socket.gethostname())
            print('host', host)
            self.mysql = Mysql(Connectable.connect_string(
                "mysql", host,
                driver="mysqldb", username='test', password='test', name='test',
                port=self.container.get_exposed_port(3306),
            ))
        else:
            connection_string = self.container.get_connection_url()
            print('connection_string', connection_string)
            self.mysql = Mysql(connection_string)

    def test_connect(self):
        self.assertEqual(Connectable.parse(self.mysql.connection_string)["driver"], "mysqldb")
        self.mysql.connect()
        self.mysql.disconnect()

    def tearDown(self):
        self.container.stop()


if __name__ == '__main__':
    unittest.main()
