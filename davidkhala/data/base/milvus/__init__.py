from typing import Literal

import pandas as pd
from davidkhala.data.base.milvus.collection import CollectionDict, Collection
from pymilvus import MilvusClient, model, CollectionSchema, FieldSchema, DataType
from davidkhala.data.base.__init__ import Connectable


def empty_schema(index_column='id', index_type: Literal[DataType.INT64, DataType.VARCHAR] = DataType.INT64,
                 **kwargs) -> CollectionSchema:
    kwargs["enable_dynamic_field"] = True  # no schema enforce
    return CollectionSchema([
        FieldSchema(name=index_column, dtype=index_type, is_primary=True, auto_id=index_type == DataType.INT64),
    ], **kwargs)


class Client(MilvusClient, Connectable):
    def __init__(self, uri: str = "http://localhost:19530",
                 user: str = "",
                 password: str = "",
                 db_name: str = "",
                 token: str = "",
                 **kwargs):
        super().__init__(uri, user, password, db_name, token, **kwargs)

        self.embedding_fn = model.DefaultEmbeddingFunction()  # small embedding model "paraphrase-albert-small-v2"

    def connect(self):
        """dry: connection established in __init__"""
        pass

    def get_collection(self, collection_name: str) -> Collection:
        return Collection(super().describe_collection(collection_name))

    def create_collection(self, collection_name: str,
                          *,
                          schema: CollectionSchema = None,
                          dimension: int = None
                          ):
        if not super().has_collection(collection_name):
            if schema:
                super().create_collection(collection_name, schema=schema)
            else:
                if not dimension:
                    dimension = self.embedding_fn.dim
                super().create_collection(collection_name, dimension)
        return self.get_collection(collection_name)

    def list_collections(self) -> list[str]:
        return super().list_collections()

    def insert_dataframe(self, collection_name: str, df: pd.DataFrame):
        super().insert(collection_name, df.to_dict(orient="records"))
