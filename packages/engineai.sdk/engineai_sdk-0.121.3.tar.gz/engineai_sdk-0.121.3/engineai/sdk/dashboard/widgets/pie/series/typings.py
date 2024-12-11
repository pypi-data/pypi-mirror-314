"""Pie Widget Series typings."""

from typing import Union

from .country import CountrySeries
from .series import Series

ChartSeries = Union[Series, CountrySeries]
