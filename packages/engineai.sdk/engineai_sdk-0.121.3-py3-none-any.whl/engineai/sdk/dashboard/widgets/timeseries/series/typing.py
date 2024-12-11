"""Specs for Timeseries series typing."""

from typing import Union

from .area import AreaSeries
from .area_range import AreaRangeSeries
from .base import TimeseriesBaseSeries
from .bubble import BubbleSeries
from .column import ColumnSeries
from .error_bar import ErrorBarSeries
from .line import LineSeries
from .point import PointSeries
from .scatter import ScatterSeries

# TODO: Same review as for CartesianSeries
TimeseriesSeries = Union[
    LineSeries,
    AreaSeries,
    AreaRangeSeries,
    ColumnSeries,
    BubbleSeries,
    ScatterSeries,
    ErrorBarSeries,
    PointSeries,
    TimeseriesBaseSeries,
]
