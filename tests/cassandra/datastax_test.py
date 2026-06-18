import unittest
from davidkhala.data.base.cassandra import Client
from davidkhala.data.base.cassandra.testcontainers import DataStax


class TestContainerBase(unittest.TestCase):
    def setUp(self) -> None:
        self.container = DataStax()
        self.container.start()

        self._ = Client(
            port=self.container.exposed_port
        )

    def tearDown(self):
        self._.close()
        self.container.stop()


class ConnectTest(TestContainerBase):
    def setUp(self) -> None:
        super().setUp()
        self._.connect()
        from davidkhala.data.base.cassandra.dba import DBA
        self.dba = DBA(self._)

    def test_query(self):
        r = self._.query("select release_version from system.local")
        self.assertEqual('4.0.0.6864', r.one()[0])

    def test_keyspaces(self):
        print(self.dba.keyspaces)
        self.dba.create_keyspace('default_keyspace', replication_factor=1)
    def test_dc(self):
        print(self.dba.hosts)
        print(self.dba.datacenter)
