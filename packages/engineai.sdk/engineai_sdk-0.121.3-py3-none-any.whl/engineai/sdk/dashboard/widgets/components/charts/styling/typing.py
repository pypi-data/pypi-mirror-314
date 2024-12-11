"""Specs for styling series in a Timeseries and Categorical widget."""

from typing import Union

from .area import AreaSeriesStyling
from .area_range import AreaRangeSeriesStyling
from .bubble_circle import BubbleCircleSeriesStyling
from .bubble_country import BubbleCountrySeriesStyling
from .column import ColumnSeriesStyling
from .error_bar import ErrorBarSeriesStyling
from .line import LineSeriesStyling
from .point import PointSeriesStyling
from .scatter import ScatterSeriesStyling

ColoredSeriesStyling = Union[
    AreaSeriesStyling,
    AreaRangeSeriesStyling,
    BubbleCircleSeriesStyling,
    ColumnSeriesStyling,
    ErrorBarSeriesStyling,
    LineSeriesStyling,
    PointSeriesStyling,
    ScatterSeriesStyling,
]

SeriesStyling = Union[ColoredSeriesStyling, BubbleCountrySeriesStyling]
