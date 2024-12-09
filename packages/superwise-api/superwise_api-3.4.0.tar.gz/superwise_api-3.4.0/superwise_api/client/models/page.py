# coding: utf-8
from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from typing import Optional

from pydantic import BaseModel
from pydantic import conint
from pydantic import conlist
from pydantic import Field
from pydantic import StrictInt
from pydantic import StrictStr
from pydantic.main import ModelMetaclass


class Page(BaseModel):
    """
    PageDatasetResponse
    """

    __model = None
    items: conlist(BaseModel) = Field(...)
    total: Optional[StrictInt] = 0
    page: conint(strict=True, ge=1) = Field(...)
    size: conint(strict=True, ge=1) = Field(...)
    next: Optional[StrictStr] = None
    previous: Optional[StrictStr] = None
    first: Optional[StrictStr] = None
    last: Optional[StrictStr] = None
    __properties = ["items", "total", "page", "size", "next", "previous", "first", "last"]

    class Config:
        """Pydantic configuration"""

        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Page:
        """Create an instance of PageDatasetResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True, exclude={}, exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in items (list)
        _items = []
        if self.items:
            for _item in self.items:
                if _item:
                    _items.append(_item.to_dict())
            _dict["items"] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Optional[Page]:
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Page.parse_obj(obj)

        _obj = Page.parse_obj(
            {
                "items": [cls.__model.from_dict(_item) for _item in obj.get("items")]
                if obj.get("items") is not None
                else None,
                "total": obj.get("total") if obj.get("total") is not None else 0,
                "page": obj.get("page"),
                "size": obj.get("size"),
                "next": obj.get("next"),
                "previous": obj.get("previous"),
                "first": obj.get("first"),
                "last": obj.get("last"),
            }
        )
        return _obj

    @classmethod
    def set_model(cls, model: ModelMetaclass):
        cls.__model = model
        return cls
