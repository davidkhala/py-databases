from typing import Dict

from cassandra.metadata import KeyspaceMetadata
from cassandra.pool import Host

from davidkhala.data.base.cassandra import Client


class DBA:

    def __init__(self, instance: Client):
        self._ = instance

    @property
    def keyspaces(self) -> Dict[str, KeyspaceMetadata]:
        return self._.client.metadata.keyspaces

    @property
    def hosts(self) -> list[Host]:
        return self._.client.metadata.all_hosts()

    @property
    def datacenter(self) -> list[str]:
        return [host.datacenter for host in self.hosts]

    def create_keyspace(self, name, *, replication_factor=None, **kwargs):

        if replication_factor:
            replication_str = f"'replication_factor': {replication_factor}"
        else:
            replication_str = ",\n  ".join(f"'{dc}': {rf}" for dc, rf in kwargs.items())

        statement = f"""
        CREATE KEYSPACE IF NOT EXISTS {name}
        WITH replication = {{
            'class': '{'SimpleStrategy' if replication_factor else 'NetworkTopologyStrategy'}',
            {replication_str}
        }}
        """
        r = self._.query(statement)
        return r
