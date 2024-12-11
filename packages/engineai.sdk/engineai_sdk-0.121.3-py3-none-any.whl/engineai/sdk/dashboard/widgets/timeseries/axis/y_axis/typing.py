"""Specs for YAxis typing."""

from typing import Union

from engineai.sdk.dashboard.widgets.timeseries.axis.y_axis.y_axis import YAxis
from engineai.sdk.dashboard.widgets.timeseries.axis.y_axis.y_axis_mirror import (
    MirrorYAxis,
)

YAxisSpec = Union[
    YAxis,
    MirrorYAxis,
]
