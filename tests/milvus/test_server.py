import os
import unittest
from pymilvus import MilvusClient


class LocalhostTestCase(unittest.TestCase):
    ...


class ZillizTestCase(unittest.TestCase):
    def setUp(self):
        self.client = MilvusClient(
            uri=os.getenv("CLUSTER_ENDPOINT", "https://in03-0eb4c55b7cd756a.serverless.gcp-us-west1.cloud.zilliz.com"),
            token=os.getenv("CLUSTER_TOKEN"),
        )

    def tearDown(self):
        self.client.close()


if __name__ == '__main__':
    unittest.main()
