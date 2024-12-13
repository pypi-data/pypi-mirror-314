from typing import Any
from typing import Optional
from typing import Union

from pydantic import BaseModel

from superwise_api.models import SuperwiseEntity


class Filter(BaseModel):
    member: str
    operator: str
    values: Optional[list[str]]


class Order(BaseModel):
    id: str
    desc: bool


class Query(SuperwiseEntity):
    measures: Optional[list[str]] = []
    order: Optional[Union[list[Order], Order]]
    dimensions: list[str] = []
    timezone: Optional[str] = "UTC"
    filters: list[Filter] = []
    timeDimensions: Optional[list[dict[str, Any]]]
    limit: Optional[int]

    def to_dict(self):
        return self.dict(exclude_none=True)
