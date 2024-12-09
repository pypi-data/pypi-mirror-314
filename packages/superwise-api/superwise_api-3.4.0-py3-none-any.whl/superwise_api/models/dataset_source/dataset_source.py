from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import Field

from superwise_api.models import SuperwiseEntity


class IngestType(str, Enum):
    INSERT = "insert"
    UPDATE = "update"


class DatasetSource(SuperwiseEntity):
    id: str = Field(...)
    source_id: str = Field(...)
    internal_dataset_id: str = Field(...)
    folder: Optional[str] = None
    query: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None
    ingest_type: Optional[IngestType] = None

    @classmethod
    def from_dict(cls, obj: dict) -> "Optional[DatasetSource]":
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return DatasetSource.parse_obj(obj)

        _obj = DatasetSource.parse_obj(
            {
                "id": obj.get("id"),
                "source_id": obj.get("source_id"),
                "internal_dataset_id": obj.get("internal_dataset_id"),
                "folder": obj.get("folder"),
                "query": obj.get("query"),
                "created_at": obj.get("created_at"),
                "updated_at": obj.get("updated_at"),
                "created_by": obj.get("created_by"),
                "ingest_type": obj.get("ingest_type"),
            }
        )
        return _obj
