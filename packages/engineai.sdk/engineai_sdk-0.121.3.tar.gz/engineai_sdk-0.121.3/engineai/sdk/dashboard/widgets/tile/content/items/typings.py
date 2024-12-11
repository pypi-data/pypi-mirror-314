"""Typing definitions for the Tile Content Items."""

from typing import Union

from .chart.area import AreaChartItem
from .chart.column import ColumnChartItem
from .chart.line import LineChartItem
from .chart.stacked_bar import StackedBarChartItem
from .date.item import DateItem
from .number.item import NumberItem
from .text.item import TextItem

TileContentItem = Union[
    NumberItem,
    DateItem,
    TextItem,
    AreaChartItem,
    ColumnChartItem,
    LineChartItem,
    StackedBarChartItem,
]
