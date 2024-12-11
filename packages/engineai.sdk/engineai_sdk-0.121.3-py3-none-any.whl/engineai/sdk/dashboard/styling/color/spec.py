"""Color spec helpers."""

from typing import Any
from typing import Dict

from engineai.sdk.dashboard.styling.color.palette import Palette

from .discrete_map import DiscreteMap
from .gradient import Gradient
from .single import Single
from .typing import ColorSpec


def build_color_spec(spec: ColorSpec) -> Dict[str, Any]:
    """Builds spec for dashboard API.

    Returns:
        Input object for Dashboard API
    """
    if isinstance(spec, Gradient):
        input_key = "gradient"
    elif isinstance(spec, DiscreteMap):
        input_key = "discreteMap"
    elif isinstance(spec, Single):
        input_key = "single"
    elif isinstance(spec, Palette):
        spec = Single(color=spec)
        input_key = "single"
    else:
        msg = "spec needs to be one of Palette, Gradient, Single, DiscreteMap."
        raise TypeError(msg)

    return {input_key: spec.build()}
