"""Specs for Axis typing."""

from typing import List
from typing import Union

from engineai.sdk.dashboard.links.widget_field import WidgetField
from engineai.sdk.dashboard.widgets.cartesian.series.typing import CartesianSeries

YAxisSeries = Union[
    str,
    List[str],
    WidgetField,
    List[WidgetField],
    CartesianSeries,
    List[CartesianSeries],
]
