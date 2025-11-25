from typing import Dict, Any

from davidkhala.data.base.milvus.format import default_index_name
from pymilvus import Collection
from pymilvus.client.types import MetricType, IndexType


def get_index(collection: Collection, index_name: str) -> Dict[str, Any]|None:
    return next(
        (
            idx.to_dict()
            for idx in collection.indexes
            if idx.index_name == index_name
        ),
        None,  # if not found
    )


def drop_index(collection: Collection, index_name: str):
    collection.release()
    collection.drop_index(index_name=index_name)


def create_index(collection: Collection, field_name: str, metric_type: MetricType,
                 *,
                 index_type=IndexType.FLAT,
                 index_name: str = None,
                 clusters=128
                 ):
    collection.create_index(
        field_name=field_name,
        index_name=index_name or default_index_name(field_name),
        index_params={
            "index_type": index_type.name,
            "metric_type": metric_type.name,  # mandatory
            "params": {"nlist": clusters}  # mandatory
        })


def search(collection: Collection, *, vector, field_name: str, limit: int, param: dict = None):
    if not param:
        metric_type = get_index(collection, default_index_name(field_name))['index_param']['metric_type']
        param = {"metric_type": metric_type}
    return collection.search(
        data=vector,
        anns_field=field_name,
        param=param,
        limit=limit
    )
