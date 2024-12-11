"""Specs for Cartesian series typing."""

from typing import Union

from .area import AreaSeries
from .area_range import AreaRangeSeries
from .base import CartesianBaseSeries
from .bubble import BubbleSeries
from .column import ColumnSeries
from .line import LineSeries
from .scatter import ScatterSeries

# TODO: Review this Union to have maybe only the BaseSeries
# but check how to have this neatly in the docs
CartesianSeries = Union[
    LineSeries,
    AreaSeries,
    AreaRangeSeries,
    ColumnSeries,
    BubbleSeries,
    ScatterSeries,
    CartesianBaseSeries,
]
