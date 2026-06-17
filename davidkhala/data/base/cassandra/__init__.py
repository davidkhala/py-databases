# To use this driver, you need A keyspace

from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT, ProtocolVersion
from cassandra.auth import PlainTextAuthProvider

from davidkhala.data.base import Connectable


class Client(Connectable):
    def __init__(self, host: str, port: int, username: str, password: str):
        super().__init__()
        self.client = Cluster(
            auth_provider=PlainTextAuthProvider("username", "password"),
            execution_profiles={EXEC_PROFILE_DEFAULT: ExecutionProfile(request_timeout=30)},
            protocol_version=ProtocolVersion.V4
        )
        self.client = Client(host, port, username, password)
    def connect(self):
        self.connection = self.client.connect()
        return True


