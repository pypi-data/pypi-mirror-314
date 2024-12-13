import json
import pprint

from pydantic import BaseModel
from pydantic.json import pydantic_encoder


class SuperwiseEntity(BaseModel):
    class Config:
        """Pydantic configuration"""

        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        return json.dumps(self.dict(), default=pydantic_encoder)

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        return self.dict(by_alias=True, exclude={}, exclude_none=True)

    @classmethod
    def from_dict(cls, obj: dict):
        raise NotImplementedError

    @classmethod
    def from_json(cls, json_str: str):
        """Create an instance of DatasetResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))
