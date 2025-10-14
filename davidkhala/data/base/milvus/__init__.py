from typing import TypedDict, Optional

from pymilvus import MilvusClient, model


class Field(TypedDict):
    field_id: int
    name: str
    description: str
    type: type
    params: dict
    is_primary: Optional[bool]
    functions: list
    aliases: list
    collection_id: int
    consistency_level: int
    properties: dict
    num_partitions: int
    enable_dynamic_field: bool
    created_timestamp: int
    update_timestamp: int


class Collection(TypedDict):
    collection_name: str
    auto_id: bool
    num_shards: int
    description: str
    fields: list[Field]


def dimension_of(c: Collection):
    return c['fields'][1]['params']['dim']


class Client:
    def __init__(self, client: MilvusClient):
        self.client = client
        self.embedding_fn = model.DefaultEmbeddingFunction()  # small embedding model "paraphrase-albert-small-v2"

    def get_collection(self, collection_name: str) -> Collection:
        return self.client.describe_collection(collection_name)

    def disconnect(self):
        self.client.close()

    def create_collection(self, collection_name: str, dimension=None):
        if not self.client.has_collection(collection_name):
            if not dimension:
                dimension = self.embedding_fn.dim
            self.client.create_collection(collection_name, dimension)
        return self.get_collection(collection_name)

    def list_collections(self) -> list[str]:
        return self.client.list_collections()
