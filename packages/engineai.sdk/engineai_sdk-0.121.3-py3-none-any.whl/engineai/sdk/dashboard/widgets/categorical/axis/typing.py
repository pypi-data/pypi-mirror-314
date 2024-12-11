"""Specs for Axis typing."""

from typing import List
from typing import Sequence
from typing import Union

from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.widgets.categorical.series.typing import CategoricalSeries

ValueAxisSeries = Union[
    str,
    List[str],
    WidgetField,
    List[WidgetField],
    CategoricalSeries,
    Sequence[CategoricalSeries],
]
