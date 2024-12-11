"""Spec to build different series supported by Map widget."""

from typing import Any
from typing import Dict

from .numeric import NumericSeries

MapSeries = NumericSeries


def build_map_series(series: MapSeries) -> Dict[str, Any]:
    """Builds spec for dashboard API.

    Args:
        series: series spec

    Returns:
        Input object for Dashboard API
    """
    if isinstance(series, NumericSeries):
        return {"numeric": series.build()}
    msg = "MapSeries requires one of MapWidgetNumericSeries, "
    raise TypeError(
        msg,
    )
