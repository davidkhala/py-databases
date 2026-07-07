from testcontainers.cassandra import CassandraContainer
from testcontainers.core.wait_strategies import HealthcheckWaitStrategy
from testcontainers.core.container import DockerContainer


class Container(CassandraContainer):
    """
    home: https://testcontainers.com/modules/cassandra/?language=python

    CassandraContainer has built-in WaitStrategy in __init__: `self.waiting_for(LogMessageWaitStrategy(wait_strategy_check_string))`
    """

    @property
    def exposed_port(self) -> int:
        return self.get_exposed_port(self.CQL_PORT)


class DataStax(DockerContainer):
    """
    for DataStax Enterprise server
    """

    def __init__(self, image: str = "datastax/dse-server:6.8.64", **kwargs):
        kwargs['healthcheck'] = {
            "test": ["CMD", "sh", "-c", "cqlsh -e 'DESCRIBE KEYSPACES;' || exit 1"]
        }
        super().__init__(image=image, **kwargs)
        self.with_exposed_ports(CassandraContainer.CQL_PORT)
        self.with_env("DS_LICENSE", 'accept')
        self.waiting_for(HealthcheckWaitStrategy())

    @property
    def exposed_port(self) -> int:
        return self.get_exposed_port(CassandraContainer.CQL_PORT)
