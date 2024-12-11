"""Specs for Tile Matrix item typing."""

from typing import Union

from .items.chart.base import BaseTileMatrixChartItem
from .items.number.item import NumberItem
from .items.text.item import TextItem

TileMatrixItem = Union[
    NumberItem,
    TextItem,
    BaseTileMatrixChartItem,
]
