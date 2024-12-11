"""Typings for Chart Item Stylings."""

from typing import Union

from .area import AreaChartItemStyling
from .column import ColumnChartItemStyling
from .line import LineChartItemStyling
from .stacked_bar import StackedBarChartItemStyling

ChartItemStyling = Union[
    AreaChartItemStyling,
    ColumnChartItemStyling,
    LineChartItemStyling,
    StackedBarChartItemStyling,
]
