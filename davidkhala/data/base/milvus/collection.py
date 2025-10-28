from typing import TypedDict

from pymilvus import DataType

from davidkhala.data.base.milvus.field import FieldDict


class CollectionDict(TypedDict):
    collection_name: str
    auto_id: bool
    num_shards: int
    description: str
    fields: list[FieldDict]


class Collection:
    def __init__(self, c: CollectionDict):
        self.c = c

    @property
    def vector_fields(self):
        return [f for f in self.c['fields'] if f['type'] in [DataType.FLOAT_VECTOR, DataType.BINARY_VECTOR]]

    @property
    def dimensions(self):
        return [f['params']['dim'] for f in self.vector_fields]
