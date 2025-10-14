import os
import unittest
from pymilvus import MilvusClient
from davidkhala.data.base.milvus import Client, dimension_of


class LocalhostTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client(MilvusClient())
    def test_connect(self):
        c_name = 'test'
        self.client.create_collection(c_name)
        collections = self.client.list_collections()
        self.assertIn(c_name , collections)
        print(collections)
    def test_drop_collection(self):
        self.client.client.drop_collection("embedding_collection")
    def test_global_connect_context(self):
        from pymilvus import connections, model, FieldSchema, DataType, Collection, CollectionSchema
        connections.connect(host='localhost', port=19530)
        embedding_fn = model.DefaultEmbeddingFunction()

        docs = [
            "Artificial intelligence was founded as an academic discipline in 1956.",
            "Alan Turing was the first person to conduct substantial research in AI.",
            "Born in Maida Vale, London, Turing was raised in southern England.",
        ]

        vectors = embedding_fn.encode_documents(docs)

        ids = []
        texts = []
        subjects = ["history"] * len(vectors)

        for i in range(len(vectors)):
            ids.append(i)
            texts.append(docs[i])

        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=768),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=512),
            FieldSchema(name="subject", dtype=DataType.VARCHAR, max_length=64),
        ]

        schema = CollectionSchema(fields)
        collection = Collection(name="embedding_collection", schema=schema)
        collection.upsert([ids, vectors, texts, subjects])
        ## For query optimize
        # collection.create_index(field_name="vector",
        #                         index_params={"index_type": "IVF_FLAT", "metric_type": "L2", "params": {"nlist": 128}})
        # collection.load()




class ZillizTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client(MilvusClient(
            uri=os.getenv("CLUSTER_ENDPOINT"),
            token=os.getenv("CLUSTER_TOKEN"),
        ))

    def test_create_collection(self):
        client = self.client.client
        collection_name = "demo_collection"
        if client.has_collection(collection_name):
            client.drop_collection(collection_name)
        self.client.create_collection(collection_name)
        c = self.client.get_collection(collection_name)

        self.assertEqual(768, dimension_of(c))

    def tearDown(self):
        self.client.disconnect()


if __name__ == '__main__':
    unittest.main()
