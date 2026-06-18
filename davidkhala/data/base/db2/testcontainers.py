from testcontainers.db2 import Db2Container


class Container(Db2Container):
    @property
    def exposed_port(self):
        return self.get_exposed_port(self.port)
