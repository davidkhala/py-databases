from typing import TypedDict


class FieldDict(TypedDict):
    field_id: int
    name: str
    description: str
    type: type
    params: dict
    is_primary: bool
    functions: list
    aliases: list
    collection_id: int
    consistency_level: int
    properties: dict
    num_partitions: int
    enable_dynamic_field: bool
    created_timestamp: int
    update_timestamp: int