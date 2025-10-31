from pymilvus import Collection
from pymilvus.client.types import MetricType, IndexType


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
        index_name=index_name or f"{field_name}_idx",
        index_params={
            "index_type": index_type.name,
            "metric_type": metric_type.name,  # mandatory
            "params": {"nlist": clusters}  # mandatory
        })
