import os
import unittest


from davidkhala.data.base.mongo import Client

class AtlasTest(unittest.TestCase):
    def setUp(self):

        db_password = os.environ.get("ATLAS_PASSWORD")
        connect_str = f"mongodb+srv://admin:{db_password}@free.csxewkh.mongodb.net/?appName=free"
        self.client = Client(connect_str)
    def test_connect(self):
        self.assertTrue(self.client.connect())

if __name__ == '__main__':
    unittest.main()