import os
import unittest

from sqlalchemy.orm import Session
from testcontainers.core.wait_strategies import HealthcheckWaitStrategy
from testcontainers.mysql import MySqlContainer
from testcontainers.postgres import PostgresContainer
from davidkhala.data.base.common import Connectable
from davidkhala.data.base.mysql import Mysql
from davidkhala.data.base.pg import Postgres
from davidkhala.data.base.pg.dba import DBA

import socket


class MysqlTestCase(unittest.TestCase):
    def setUp(self):
        self.container = MySqlContainer()
        self.container.start()
        self.container.waiting_for(HealthcheckWaitStrategy())
        if os.environ.get("CI"):
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

class PostgresTestCase(unittest.TestCase):
    def setUp(self):
        self.container = PostgresContainer("postgres")  # 可以指定版本
        self.container.start()
        self.container.waiting_for(HealthcheckWaitStrategy())
        if os.environ.get("CI"):
            host = socket.gethostbyname(socket.gethostname())
            print('host', host)
            self.pg = Postgres(Connectable.connect_string(
                "postgresql", host,
                driver="psycopg2", username='test', password='test', name='test',
                port=self.container.get_exposed_port(5432),
            ))
        else:
            connection_string = self.container.get_connection_url()
            print('connection_string', connection_string)
            self.pg = Postgres(connection_string)

    def test_connect(self):
        self.assertEqual(Connectable.parse(self.pg.connection_string)["driver"], "psycopg2")
        self.pg.connect()
        self.pg.disconnect()

    def test_databases(self):
        self.pg.connect()
        dba = DBA(self.pg)
        self.assertListEqual(['postgres', 'test'], dba.databases)
        self.pg.disconnect()
    def test_tx(self):
        self.pg.connect()
        with Session(self.pg.client) as session:
            session.commit()
        self.pg.disconnect()


    def tearDown(self):
        self.container.stop()

if __name__ == '__main__':
    unittest.main()
