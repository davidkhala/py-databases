import os
import socket
import unittest

from sqlalchemy.orm import Session
from testcontainers.core.wait_strategies import HealthcheckWaitStrategy

from davidkhala.data.base.pg import Postgres
from davidkhala.data.base.pg.dba import DBA
from davidkhala.data.base.pg.testcontainers import Container as PostgresContainer
from davidkhala.data.base.sql import SQL


class PostgresTestCase(unittest.TestCase):
    def setUp(self):
        self.container = PostgresContainer()
        self.container.waiting_for(HealthcheckWaitStrategy())
        self.container.start()
        if os.environ.get("CI"):
            host = socket.gethostbyname(socket.gethostname())
            print('host', host)
            self.pg = Postgres(SQL.connect_string(
                "postgresql", host,
                driver="psycopg2", username='test', password='test', name='test',
                port=self.container.get_exposed_port(5432),
            ))
        else:
            connection_string = self.container.get_connection_url()
            print('connection_string', connection_string)
            self.pg = Postgres(connection_string)

    def test_connect(self):
        self.assertEqual(SQL.parse(self.pg.connection_string)["driver"], "psycopg2")
        self.pg.connect()
        self.pg.close()

    def test_databases(self):
        self.pg.connect()
        dba = DBA(self.pg)
        self.assertListEqual(['postgres', 'test'], dba.databases)
        self.pg.close()

    def test_tx(self):
        host = socket.gethostbyname(socket.gethostname())
        with Postgres(SQL.connect_string(
                "postgresql", host,
                driver="psycopg2", username='test', password='test', name='test',
                port=self.container.get_exposed_port(5432),
        )) as pg:
            with Session(pg.client) as session:
                session.commit()

    def tearDown(self):
        self.container.stop()
if __name__ == '__main__':
    unittest.main()