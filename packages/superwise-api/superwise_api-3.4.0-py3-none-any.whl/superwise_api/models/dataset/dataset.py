from datetime import datetime
from typing import Optional

from pydantic import Field

from superwise_api.models import SuperwiseEntity
from superwise_api.models.dataset.dataset_schema import DatasetSchema


class Dataset(SuperwiseEntity):
    id: Optional[str] = Field(...)
    name: Optional[str] = Field(..., description="A descriptive name for this dataset")
    description: Optional[str] = Field(None, description="Relevant information about the context of this dataset")
    model_version_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = Field(...)
    tenant_id: Optional[str] = None
    dataset_schema: Optional[DatasetSchema] = Field({}, alias="schema")
    internal_id: Optional[str] = Field(..., alias="_id")

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True, exclude={}, exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of var_schema
        if self.dataset_schema:
            _dict["schema"] = self.dataset_schema.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> "Optional[Dataset]":
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Dataset.parse_obj(obj)

        _obj = Dataset.parse_obj(
            {
                "_id": obj.get("_id"),
                "id": obj.get("id"),
                "name": obj.get("name"),
                "description": obj.get("description"),
                "model_version_id": obj.get("model_version_id"),
                "created_at": obj.get("created_at"),
                "updated_at": obj.get("updated_at"),
                "created_by": obj.get("created_by"),
                "dataset_schema": DatasetSchema.from_dict(obj.get("schema"))
                if obj.get("schema")
                else obj.get("dataset_schema"),
            }
        )
        return _obj
