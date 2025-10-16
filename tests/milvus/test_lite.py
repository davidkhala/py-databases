import platform
import unittest

from pymilvus import MilvusClient, model, CollectionSchema, DataType
from pymilvus.exceptions import PrimaryKeyException

from davidkhala.data.base.milvus import empty_schema


class HeadlessTestCase(unittest.TestCase):
    def test_data_prep(self):
        embedding_fn = model.DefaultEmbeddingFunction()  # small embedding model "paraphrase-albert-small-v2"
        self.assertEqual(768, embedding_fn.dim)

        docs = [
            "Artificial intelligence was founded as an academic discipline in 1956.",
            "Alan Turing was the first person to conduct substantial research in AI.",
            "Born in Maida Vale, London, Turing was raised in southern England.",
        ]

        vectors = embedding_fn.encode_documents(docs)

        self.assertEqual(embedding_fn.dim, len(vectors[0]))
    def test_schema(self):
        with self.assertRaises(PrimaryKeyException) as e:
            CollectionSchema([])
        self.assertEqual('Schema must have a primary key field.', e.exception.message)
        empty_schema()
        empty_schema('id', DataType.INT64)
        empty_schema('uid', DataType.VARCHAR)
        with self.assertRaises(PrimaryKeyException) as e:
            empty_schema('-', DataType.STRING)
        self.assertEqual('Primary key type must be DataType.INT64 or DataType.VARCHAR.', e.exception.message)
class LiteTestCase(unittest.TestCase):
    """https://milvus.io/docs/quickstart.md#Set-Up-Vector-Database"""

    def setUp(self):
        self.client: MilvusClient

    def test_windows(self):
        # Milvus Lite does not support windows
        if platform.system() == "Windows":
            with self.assertRaises(ModuleNotFoundError):
                self.client = MilvusClient("milvus_demo.db")


if __name__ == '__main__':
    unittest.main()
