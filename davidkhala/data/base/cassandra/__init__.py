# To use this driver, you need A keyspace
from typing import Dict, Any

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT, ProtocolVersion, Session, ResultSet
from cassandra.metadata import KeyspaceMetadata

from davidkhala.data.base import Connectable


class Client(Connectable):
    def __init__(self, host='localhost', *, username=None, password=None, port=9042):
        super().__init__()

        options = {}
        if username and password:
            options['auth_provider'] = PlainTextAuthProvider(username=username, password=password)

        self.client = Cluster(
            execution_profiles={EXEC_PROFILE_DEFAULT: ExecutionProfile(request_timeout=30)},
            protocol_version=ProtocolVersion.V4,
            contact_points=[host],
            port=port,
            **options
        )

    def connect(self):
        self.connection: Session = self.client.connect()
        return True

    def close(self):
        self.connection.shutdown()
        del self.connection

    def query(self,
              template: str,
              values: Dict[str, Any] | None = None,
              request_options: Dict[str, Any] | None = None
              )-> ResultSet:
        return self.connection.execute(
            template, values, **(request_options or {})
        )
