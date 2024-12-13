from datetime import datetime

from superwise_api.models import SuperwiseEntity


class SlackDestinationParams(SuperwiseEntity):
    channel_id: str

    def to_dict(self):
        return self.dict()


class Destination(SuperwiseEntity):
    id: str
    name: str
    integration_id: str
    params: SlackDestinationParams
    updated_at: datetime
    created_at: datetime
    created_by: str
    tenant_id: str

    def to_dict(self) -> dict:
        dict_ = self.dict(exclude_none=True)
        return dict_

    @classmethod
    def from_dict(cls, dict_: dict) -> "Destination":
        dict_["params"] = SlackDestinationParams(**dict_["params"])
        return cls(**dict_)
