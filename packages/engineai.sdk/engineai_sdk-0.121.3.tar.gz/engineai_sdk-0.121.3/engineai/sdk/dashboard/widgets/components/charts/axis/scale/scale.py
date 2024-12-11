"""Spec to build different scales supported by y axis."""

from typing import Any
from typing import Dict

from .dynamic import AxisScaleDynamic
from .negative import AxisScaleNegative
from .positive import AxisScalePositive
from .symmetric import AxisScaleSymmetric
from .typing import AxisScale


def build_axis_scale(scale: AxisScale) -> Dict[str, Any]:
    """Builds spec for dashboard API.

    Returns:
        Input object for Dashboard API
    """
    return {_get_input_key(scale): scale.build()}


def _get_input_key(scale: AxisScale) -> str:
    if isinstance(scale, AxisScaleDynamic):
        return "dynamic"
    if isinstance(scale, AxisScaleSymmetric):
        return "symmetrical"
    if isinstance(scale, AxisScalePositive):
        return "positive"
    if isinstance(scale, AxisScaleNegative):
        return "negative"
    msg = (
        "AxisScale requires one of AxisScaleDynamic, "
        "AxisScaleDynamic, AxisScalePositive, "
        "AxisScaleNegative"
    )
    raise TypeError(msg)
