from enum import Enum
from typing import Any
from typing import Optional

from superwise_api.models import SuperwiseEntity


class SchemaItemType(str, Enum):
    NUMERIC = "numeric"
    STRING = "string"
    BOOLEAN = "boolean"
    DATETIME = "datetime"
    DATE = "date"


class SchemaItem(SuperwiseEntity):
    type: Optional[SchemaItemType]
    default_value: Optional[Any] = None


class DatasetSchema(SuperwiseEntity):
    """
    DatasetSchema
    """

    fields: Optional[Any] = None
    key_field: Optional[str] = None
    __properties = ["fields", "key_field"]

    @classmethod
    def from_dict(cls, obj: dict) -> "Optional[DatasetSchema]":
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return DatasetSchema.parse_obj(obj)

        _obj = DatasetSchema.parse_obj(
            {
                "key_field": obj.get("key_field"),
                "timestamp_partition_field": obj.get("timestamp_partition_field"),
                "fields": obj.get("fields"),
            }
        )
        return _obj
