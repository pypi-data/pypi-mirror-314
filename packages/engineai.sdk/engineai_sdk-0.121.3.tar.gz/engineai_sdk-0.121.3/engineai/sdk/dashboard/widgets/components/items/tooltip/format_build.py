"""Spec to build different items supported by tile widget."""

from typing import Any
from typing import Dict

from engineai.sdk.dashboard.formatting import DateTimeFormatting
from engineai.sdk.dashboard.formatting import MapperFormatting
from engineai.sdk.dashboard.formatting import NumberFormatting
from engineai.sdk.dashboard.formatting import TextFormatting
from engineai.sdk.dashboard.widgets.components.charts.tooltip.base import (
    TooltipItemFormatter,
)


def build_items(item: TooltipItemFormatter) -> Dict[str, Any]:
    """Builds spec for dashboard API.

    Args:
        item (TileItem): item spec

    Returns:
        Input object for Dashboard API
    """
    return {_get_input_key(item): item.build()}


def _get_input_key(item: TooltipItemFormatter) -> str:
    if isinstance(item, TextFormatting):
        result = "text"
    elif isinstance(item, NumberFormatting):
        result = "number"
    elif isinstance(item, MapperFormatting):
        result = "mapper"
    elif isinstance(item, DateTimeFormatting):
        result = "dateTime"
    else:
        msg = (
            "Formatting requires one of TextFormatting, NumberFormatting, "
            "MapperFormatting, DateTimeFormatting."
        )
        raise TypeError(msg)
    return result
