import os
import unittest

from pymilvus import MilvusClient, MilvusException
from pymilvus import connections, model, FieldSchema, DataType, Collection, CollectionSchema, has_collection
from pymilvus.client.types import MetricType

from davidkhala.data.base.milvus import Client, empty_schema
from davidkhala.data.base.milvus.inline import create_index, get_index, search
from davidkhala.data.base.milvus.format import default_index_name


class LocalhostTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client(MilvusClient())

    def test_collections(self):
        c_name = 'test'
        self.client.create_collection(c_name)
        collections = self.client.list_collections()
        self.assertIn(c_name, collections)
        print(collections)

    def test_drop_collection(self):
        self.client.client.drop_collection("embedding_collection")
        self.client.client.create_schema()

    def test_global_connect_context(self):

        connections.connect(host='localhost', port=19530)
        embedding_fn = model.DefaultEmbeddingFunction()

        collection_name = "embedding_collection"

        if not has_collection(collection_name):

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
            collection = Collection(name=collection_name, schema=schema)
            collection.upsert([ids, vectors, texts, subjects])
        else:
            collection = Collection(name=collection_name)

        if not collection.has_index(index_name='vector'):
            ## For query optimize
            create_index(collection, "vector", metric_type=MetricType.IP)
            collection.load()

        results = search(collection,
            vector=embedding_fn.encode_documents(['what happened in 1956']),
            field_name='vector',
            limit=2
        )

        best_hit = max(results[0], key=lambda x: x.distance)  # 如果是 IP 或 COSINE，相似度越高越好
        print(best_hit)
    def test_get_index(self):
        connections.connect(host='localhost', port=19530)
        field = 'vector'
        collection_name ="embedding_collection"
        if has_collection(collection_name):
            collection = Collection(name=collection_name)
            r = get_index(collection, default_index_name(field) )
            print(r)

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
        self.assertIn(768, c.dimensions)
        print(c)

    def test_create_schema_collection(self):
        client = self.client.client
        collection_name = "collection"
        if client.has_collection(collection_name):
            client.drop_collection(collection_name)
        #
        schema = empty_schema()
        with self.assertRaises(MilvusException) as e:
            self.client.create_collection(collection_name, schema=schema)
        self.assertEqual('schema does not contain vector field: invalid parameter', e.exception.message)

    def tearDown(self):
        self.client.close()


if __name__ == '__main__':
    unittest.main()
