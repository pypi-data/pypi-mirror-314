"""Spec for Color resources."""

from .default_specs import PositiveNegativeDiscreteMap
from .discrete_map import DiscreteMap
from .discrete_map import DiscreteMapIntervalItem
from .discrete_map import DiscreteMapValueItem
from .divergent import Divergent
from .gradient import Gradient
from .gradient import GradientItem
from .palette import Palette
from .palette import PaletteTypes
from .single import Single

__all__ = [
    # .single
    "Single",
    # .discrete_map
    "DiscreteMap",
    "DiscreteMapValueItem",
    "DiscreteMapIntervalItem",
    # .gradient
    "Gradient",
    "GradientItem",
    # .palette
    "PaletteTypes",
    "Palette",
    # .default_specs
    "PositiveNegativeDiscreteMap",
    # .divergent
    "Divergent",
]
