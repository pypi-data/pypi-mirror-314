"""Spec for Widget Stacked Bar Chart Styling."""

from typing import Any
from typing import Dict

from engineai.sdk.dashboard.widgets.components.items.styling.base import BaseItemStyling


class StackedBarChartItemStyling(BaseItemStyling):
    """Spec for styling used by Stacked Bar Chart Item."""

    def _build_extra_inputs(self) -> Dict[str, Any]:
        return {"showTotalOnTooltip": False}
