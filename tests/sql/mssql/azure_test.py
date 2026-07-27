import os
import unittest
from pathlib import Path

import certifi
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs

from davidkhala.data.base.mssql.with_odbc import ConnectString, ColdClient
from davidkhala.data.base.mssql.with_tds import Client, ProxyConfig, ProxyType


class AzureTestCase(unittest.TestCase):
    def setUp(self):
        self.password = os.environ.get("MSSQL_PASSWORD")
        queries = {
            "Encrypt": "yes",
        }
        self.domain = 'sql-server-hk.database.windows.net'
        self.dbname = 'mssql'
        self.username = 'CloudSA7b5eda98'
        self.odbc_client = ColdClient(ConnectString.build(
            self.domain,
            username=self.username,
            password=self.password,
            dbname=self.dbname,
            queries=queries
        ))
        # wait for warmup
        self.odbc_client.connect()


    def test_proxy(self):
        # 1. Start a Squid proxy container with a custom config that allows
        #    CONNECT tunneling to port 1433 (MSSQL), which Squid blocks by default.
        SQUID_PORT = 3128
        squid_conf = Path(__file__).parent / "squid.conf"
        squid = (
            DockerContainer("ubuntu/squid:latest")
            .with_volume_mapping(str(squid_conf), "/etc/squid/squid.conf", "ro")
            .with_exposed_ports(SQUID_PORT)
        )
        with squid:
            # Wait until Squid is ready to accept connections
            wait_for_logs(squid, r"listening port", timeout=30)

            proxy_host = squid.get_container_host_ip()
            proxy_port = int(squid.get_exposed_port(SQUID_PORT))

            # 2. Connect to Azure SQL DB through the Squid HTTP proxy
            proxy_config: ProxyConfig = {
                "type": ProxyType.HTTP,
                "host": proxy_host,
                "port": proxy_port,
            }
            client = Client(
                domain=self.domain,
                username=self.username,
                password=self.password,
                name=self.dbname,
                proxy=proxy_config,
                connect_kwargs={
                    "cafile": certifi.where(),
                    "validate_host": False,
                }
            )
            self.assertTrue(client.connect())
