import unittest

from davidkhala.data.base.cassandra import Client
from davidkhala.data.base.cassandra.testcontainers import Container

class LocalTest(unittest.TestCase):
    def setUp(self):
        self.container = Container()
        self.container.start()

        self._ = Client(
            username="cassandra",
            password="cassandra",
            port=self.container.exposed_port
        )
    def tearDown(self):
        self._.close()
        self.container.stop()

class ConnectTest(LocalTest):
    def test_connect(self):
        self._.connect()

