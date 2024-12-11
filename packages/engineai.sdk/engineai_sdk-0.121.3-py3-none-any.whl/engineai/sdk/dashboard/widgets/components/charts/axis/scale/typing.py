"""Specs for Scale in Chart Axis ."""

from typing import Union

from .dynamic import AxisScaleDynamic
from .negative import AxisScaleNegative
from .positive import AxisScalePositive
from .symmetric import AxisScaleSymmetric

AxisScale = Union[
    AxisScaleDynamic,
    AxisScaleSymmetric,
    AxisScalePositive,
    AxisScaleNegative,
]
