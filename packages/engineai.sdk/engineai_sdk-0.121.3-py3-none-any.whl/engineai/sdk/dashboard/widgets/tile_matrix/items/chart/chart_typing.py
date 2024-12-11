"""Specs for chart typing."""

from typing import Union

from engineai.sdk.dashboard.widgets.components.items.styling import AreaChartItemStyling
from engineai.sdk.dashboard.widgets.components.items.styling import (
    ColumnChartItemStyling,
)
from engineai.sdk.dashboard.widgets.components.items.styling import LineChartItemStyling
from engineai.sdk.dashboard.widgets.components.items.styling import (
    StackedBarChartItemStyling,
)

TileMatrixChartStyling = Union[
    AreaChartItemStyling,
    ColumnChartItemStyling,
    LineChartItemStyling,
    StackedBarChartItemStyling,
]
