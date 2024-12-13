from datetime import datetime
from typing import Optional

from pydantic import Field
from pydantic import UUID4

from superwise_api.models import SuperwiseEntity
from superwise_api.models.dataset import Dataset


class Model(SuperwiseEntity):
    id: str
    internal_id: Optional[UUID4] = Field(..., alias="_id")
    name: str
    description: Optional[str]
    created_by: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True, exclude={}, exclude_none=True)
        _dict["_id"] = str(_dict["_id"])
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> "Optional[Model]":
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Model.parse_obj(obj)

        _obj = Model.parse_obj(
            {
                "_id": obj.get("_id"),
                "id": obj.get("id"),
                "name": obj.get("name"),
                "description": obj.get("description"),
                "created_at": obj.get("created_at"),
                "updated_at": obj.get("updated_at"),
                "created_by": obj.get("created_by"),
            }
        )
        return _obj


class ModelExtended(Model):
    datasets: list[Dataset]

    @classmethod
    def from_dict(cls, obj: dict) -> "Optional[ModelExtended]":
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ModelExtended.parse_obj(obj)

        _obj = ModelExtended.parse_obj(
            {
                "_id": obj.get("_id"),
                "id": obj.get("id"),
                "name": obj.get("name"),
                "description": obj.get("description"),
                "created_at": obj.get("created_at"),
                "updated_at": obj.get("updated_at"),
                "created_by": obj.get("created_by"),
                "datasets": [Dataset.from_dict(dataset) for dataset in obj.get("datasets")],
            }
        )
        return _obj
