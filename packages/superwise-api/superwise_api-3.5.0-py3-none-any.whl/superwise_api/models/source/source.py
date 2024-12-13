from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from superwise_api.models import SuperwiseEntity

GCS_BUCKET_REGEX = r"^[a-z0-9][a-z0-9_-]{1,61}[a-z0-9](\.[a-z0-9][a-z0-9_-]{1,61}[a-z0-9])*$"
PUBSUB_TOPIC_REGEX = r"^projects\/[a-z][a-z0-9-]{3,29}\/topics\/[a-zA-Z][-\w.~%+]{2,254}$"
S3_BUCKET_REGEX = r"^arn:aws(-cn|-us-gov)?:s3:([a-z]{2}(-gov)?-[a-z]+-\d)?:(\d{12})?:[0-9a-z][0-9a-z.-]{2,62}$"
SQS_QUEUE_REGEX = r"^arn:aws(-cn|-us-gov)?:sqs:[a-z]{2}(-gov)?-[a-z]+-\d:\d{12}:.+$"


class SourceType(str, Enum):
    GCS = "GCS"
    S3 = "S3"


class Source(SuperwiseEntity):
    id: Optional[str]
    name: Optional[str]

    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    created_by: Optional[str]

    type: Optional[SourceType]
    params: Optional[dict]
    credentials: Optional[dict]

    __properties = [
        "id",
        "name",
        "created_at",
        "updated_at",
        "created_by",
        "type",
        "params",
        "credentials",
    ]

    @classmethod
    def from_dict(cls, obj: dict) -> Optional["Source"]:
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Source.parse_obj(obj)

        _obj = Source.parse_obj(
            {
                "id": obj.get("id"),
                "name": obj.get("name"),
                "created_at": obj.get("created_at"),
                "updated_at": obj.get("updated_at"),
                "created_by": obj.get("created_by"),
                "type": obj.get("type"),
                "params": obj.get("params"),
                "credentials": obj.get("credentials"),
            }
        )
        return _obj
