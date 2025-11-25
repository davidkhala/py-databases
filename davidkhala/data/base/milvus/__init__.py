from typing import Literal

import pandas as pd
from davidkhala.data.base.milvus.collection import CollectionDict, Collection
from pymilvus import MilvusClient, model, CollectionSchema, FieldSchema, DataType


def empty_schema(index_column='id', index_type: Literal[DataType.INT64, DataType.VARCHAR] = DataType.INT64,
                 **kwargs) -> CollectionSchema:
    kwargs["enable_dynamic_field"] = True  # no schema enforce
    return CollectionSchema([
        FieldSchema(name=index_column, dtype=index_type, is_primary=True, auto_id=index_type == DataType.INT64),
    ], **kwargs)


class Client:
    def __init__(self, client: MilvusClient):
        self.client = client
        self.embedding_fn = model.DefaultEmbeddingFunction()  # small embedding model "paraphrase-albert-small-v2"

    def get_collection(self, collection_name: str) -> Collection:
        return Collection(self.client.describe_collection(collection_name))

    def disconnect(self):
        self.client.close()

    def create_collection(self, collection_name: str,
                          *,
                          schema: CollectionSchema = None,
                          dimension: int = None
                          ):
        if not self.client.has_collection(collection_name):
            if schema:
                self.client.create_collection(collection_name, schema=schema)
            else:
                if not dimension:
                    dimension = self.embedding_fn.dim
                self.client.create_collection(collection_name, dimension)
        return self.get_collection(collection_name)

    def list_collections(self) -> list[str]:
        return self.client.list_collections()

    def insert_dataframe(self, collection_name: str, df: pd.DataFrame):
        self.client.insert(collection_name, df.to_dict(orient="records"))
