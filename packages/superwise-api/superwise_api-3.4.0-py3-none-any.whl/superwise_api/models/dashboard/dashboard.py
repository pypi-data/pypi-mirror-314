from datetime import datetime
from enum import Enum
from typing import Dict
from typing import Optional

from superwise_api.models import SuperwiseEntity


class VisualizationType(str, Enum):
    TABLE = "table"
    LINE_GRAPH = "line_graph"
    BAR_PLOT = "bar_plot"
    TIME_SERIES = "time_series"
    HISTOGRAM = "histogram"


class WidgetMeta(SuperwiseEntity):
    visualization_type: VisualizationType
    x_pos: int
    y_pos: int
    height: int = 0
    width: int = 0


class Dashboard(SuperwiseEntity):
    id: Optional[str]
    name: str
    created_by: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    positions: Optional[Dict[str, WidgetMeta]]

    @classmethod
    def from_dict(cls, obj: dict) -> "Optional[Dashboard]":
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Dashboard.parse_obj(obj)

        _obj = Dashboard.parse_obj(
            {
                "id": obj.get("id"),
                "name": obj.get("name"),
                "created_by": obj.get("created_by"),
                "created_at": obj.get("created_at"),
                "updated_at": obj.get("updated_at"),
                "positions": {k: WidgetMeta.parse_obj(v) for k, v in obj.get("positions", {}).items()},
            }
        )
        return _obj
