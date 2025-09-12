import unittest
from pymilvus import MilvusClient, model

from tests.milvus.cases import create_collection, prepare_data

class HeadlessTestCase(unittest.TestCase):
    def test_data_prep(self):
        prepare_data()
class QuickStartTestCase(unittest.TestCase):
    """https://milvus.io/docs/quickstart.md#Set-Up-Vector-Database"""
    def setUp(self):
        # Milvus Lite does not support windows
        self.client = MilvusClient("milvus_demo.db")
    def test_create_collection(self):
        create_collection(self.client)
    def tearDown(self):
        self.client.close()

if __name__ == '__main__':
    unittest.main()