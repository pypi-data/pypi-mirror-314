from datetime import datetime
from enum import Enum
from typing import Literal
from typing import Optional
from typing import Union

from pydantic import BaseModel
from pydantic import Field
from pydantic import PositiveFloat
from pydantic import PositiveInt

from superwise_api.models import SuperwiseEntity
from superwise_api.models.policy.query import Query


class TimeRangeUnit(str, Enum):
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"


class DataConfigType(str, Enum):
    STATISTICS = "statistics"
    DISTRIBUTION_COMPARE = "distribution_compare"


class DistanceFunction(str, Enum):
    WASSERSTEIN_DISTANCE = "wasserstein_distance"
    JENSEN_SHANNON_DIVERGENCE = "jensen_shannon_divergence"


class TimeRangeConfig(BaseModel):
    field_name: str
    unit: TimeRangeUnit
    value: int


class DataConfigBase(SuperwiseEntity):
    type: DataConfigType


class DataConfigStatistics(DataConfigBase):
    type: Literal[DataConfigType.STATISTICS] = DataConfigType.STATISTICS
    query: Query
    time_range_config: TimeRangeConfig


class DataConfigDistributionCompare(DataConfigBase):
    type: Literal[DataConfigType.DISTRIBUTION_COMPARE] = DataConfigType.DISTRIBUTION_COMPARE
    query_a: Query
    query_b: Query
    query_a_time_range_config: Optional[TimeRangeConfig] = None
    query_b_time_range_config: Optional[TimeRangeConfig] = None
    distance_function: DistanceFunction


# Threshold-related models remain unchanged
class ThresholdTypes(str, Enum):
    STATIC = "static"
    MOVING_AVERAGE = "moving_average"


class ThresholdSettings(BaseModel):
    threshold_type: Literal["static", "moving_average"] = Field(...)

    def to_dict(self) -> dict:
        return self.dict(exclude_none=True)


class StaticThresholdSettings(ThresholdSettings):
    condition_above_value: Optional[float]
    condition_below_value: Optional[float]
    threshold_type: Literal["static"] = "static"


class MovingAverageThresholdSettings(ThresholdSettings):
    is_violation_above: bool = True
    is_violation_below: bool = True
    violation_deviation: PositiveFloat
    threshold_type: Literal["moving_average"] = "moving_average"
    window_size: PositiveInt


class AlertOnStatusDirection(str, Enum):
    HEALTHY_TO_UNHEALTHY = "HEALTHY_TO_UNHEALTHY"
    UNHEALTHY_TO_HEALTHY = "UNHEALTHY_TO_HEALTHY"
    BOTH = "BOTH"


class Policy(SuperwiseEntity):
    id: str
    name: str
    data_config: Union[DataConfigStatistics, DataConfigDistributionCompare]
    cron_expression: str
    threshold_settings: Union[StaticThresholdSettings, MovingAverageThresholdSettings] = Field(
        discriminator="threshold_type"
    )
    alert_on_status: AlertOnStatusDirection
    alert_on_policy_level: bool
    dataset_id: str
    destination_ids: list[str]
    last_evaluation: Optional[datetime]
    next_evaluation: Optional[datetime]
    status: Optional[str]
    status_reason: Optional[dict] = None
    created_by: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    tenant_id: str

    def to_dict(self) -> dict:
        dict_ = self.dict(exclude_none=True)
        return dict_

    @classmethod
    def from_dict(cls, dict_: dict) -> "Policy":
        data_config_type = dict_["data_config"]["type"]
        if data_config_type == DataConfigType.STATISTICS:
            dict_["data_config"] = DataConfigStatistics(**dict_["data_config"])
        elif data_config_type == DataConfigType.DISTRIBUTION_COMPARE:
            dict_["data_config"] = DataConfigDistributionCompare(**dict_["data_config"])
        else:
            raise ValueError(f"Unknown data_config type: {data_config_type}")

        if dict_["threshold_settings"]["threshold_type"] == ThresholdTypes.STATIC:
            dict_["threshold_settings"] = StaticThresholdSettings(**dict_["threshold_settings"])
        else:
            dict_["threshold_settings"] = MovingAverageThresholdSettings(**dict_["threshold_settings"])
        return cls(**dict_)
