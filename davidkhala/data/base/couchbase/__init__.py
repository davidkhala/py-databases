from datetime import timedelta
from typing import Union

from couchbase.auth import PasswordAuthenticator
from couchbase.bucket import Bucket
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from davidkhala.data.base.common import Connectable

class Couchbase(Connectable):
    def __init__(self, password: str, username="Administrator", domain='localhost', tls=True):
        dialect = 'couchbases' if tls else 'couchbase'
        self.connection_string = f"{dialect}://{domain}"
        self.options = ClusterOptions(PasswordAuthenticator(
            username,
            password,
        ))
        self.connection: Cluster | None = None
        self.bucket_name: str | None = None
        self.bucket: Bucket | None = None

    def connect(self):
        self.connection = Cluster(self.connection_string, self.options)
        self.connection.wait_until_ready(timedelta(seconds=5))
        if self.bucket_name is not None:
            self.bucket = self.connection.bucket(bucket)

    def close(self, exc_type, exc_val, exc_tb):
        del self.bucket
        self.connection.close()
