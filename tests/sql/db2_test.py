import unittest

from testcontainers.core.wait_strategies import HealthcheckWaitStrategy

from davidkhala.data.base.db2.testcontainers import Container
from sqlalchemy import create_engine, text

class DB2TestCase(unittest.TestCase):
    def setUp(self):
        self.container = Container()
        self.container.start()
    def test_connect(self):
        engine = create_engine(self.container.get_connection_url())
        with engine.begin() as connection:
            result = connection.execute(text("select service_level from sysibmadm.env_inst_info"))
            print(result.fetchall())
        connection.close()
    def tearDown(self):
        self.container.stop()
if __name__ == '__main__':
    unittest.main()
