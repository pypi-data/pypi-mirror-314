"""Specs for default color specs."""

import sys
from typing import Any
from typing import ClassVar

from engineai.sdk.dashboard.styling.color.palette import (
    PercentageAllNegativeSequentialPalette,
)
from engineai.sdk.dashboard.styling.color.palette import (
    PercentageAllPositiveSequentialPalette,
)
from engineai.sdk.dashboard.styling.color.palette import SequentialPalette
from engineai.sdk.dashboard.styling.color.palette import sequential_palette

from .discrete_map import DiscreteMap
from .discrete_map import DiscreteMapIntervalItem
from .discrete_map import DiscreteMapValueItem
from .gradient import Gradient
from .gradient import GradientItem
from .single import Palette
from .single import Single


class PositiveNegativeDiscreteMap(DiscreteMap):
    """Template for discrete map with positive/negative numbers.

    Template for creating a discrete map specifically designed
    for positive and negative numbers.
    """

    def __init__(self) -> None:
        """Constructor for PositiveNegativeDiscreteMap."""
        super().__init__(
            DiscreteMapIntervalItem(
                color=Palette.RUBI_RED,
                min_value=-sys.maxsize,
                max_value=0,
                exclude_max=True,
            ),
            DiscreteMapValueItem(value=0, color=Palette.COCONUT_GREY),
            DiscreteMapIntervalItem(
                color=Palette.OCEAN_BLUE,
                min_value=0,
                max_value=sys.maxsize,
                exclude_min=True,
            ),
        )


class PercentageAllPositiveSequentialColorGradient(Gradient):
    """Percentage All Positive Sequential Color Gradient."""

    def __init__(self) -> None:
        """Creates template Percentage All Positive Sequential Color Gradient spec."""
        palette = PercentageAllPositiveSequentialPalette
        super().__init__(
            GradientItem(
                color=Single(color=sequential_palette(index=0, palette=palette)),
                value=0,
            ),
            GradientItem(
                color=Single(color=sequential_palette(index=1, palette=palette)),
                value=1 / 5,
            ),
            GradientItem(
                color=Single(color=sequential_palette(index=2, palette=palette)),
                value=2 / 5,
            ),
            GradientItem(
                color=Single(color=sequential_palette(index=3, palette=palette)),
                value=3 / 5,
            ),
            GradientItem(
                color=Single(color=sequential_palette(index=4, palette=palette)),
                value=4 / 5,
            ),
            steps=5,
        )


class PercentageAllNegativeSequentialColorGradient(Gradient):
    """Percentage All Negative Sequential Color Gradient."""

    def __init__(self) -> None:
        """Creates template Percentage All Negative Sequential Color Gradient spec."""
        palette = PercentageAllNegativeSequentialPalette
        super().__init__(
            GradientItem(
                color=Single(color=sequential_palette(index=4, palette=palette)),
                value=-1,
            ),
            GradientItem(
                color=Single(color=sequential_palette(index=3, palette=palette)),
                value=-4 / 5,
            ),
            GradientItem(
                color=Single(color=sequential_palette(index=2, palette=palette)),
                value=-3 / 5,
            ),
            GradientItem(
                color=Single(color=sequential_palette(index=1, palette=palette)),
                value=-2 / 5,
            ),
            GradientItem(
                color=Single(color=sequential_palette(index=0, palette=palette)),
                value=-1 / 5,
            ),
            steps=5,
        )


class SequentialColorGradient(Gradient):
    """Sequential discrete map."""

    def __init__(self, palette: Any = SequentialPalette) -> None:
        """Creates template Sequential Color Map spec."""
        super().__init__(
            GradientItem(
                color=Single(color=sequential_palette(index=5, palette=palette)),
                value=0,
            ),
            GradientItem(
                color=Single(color=sequential_palette(index=4, palette=palette)),
                value=1 / 5,
            ),
            GradientItem(
                color=Single(color=sequential_palette(index=3, palette=palette)),
                value=2 / 5,
            ),
            GradientItem(
                color=Single(color=sequential_palette(index=2, palette=palette)),
                value=0.5,
            ),
            GradientItem(
                color=Single(color=sequential_palette(index=1, palette=palette)),
                value=4 / 5,
            ),
            GradientItem(
                color=Single(color=sequential_palette(index=0, palette=palette)),
                value=1,
            ),
            steps=5,
        )


class ScoreColorDiscreteMap(DiscreteMap):
    """Score Color Discrete Map."""

    SCORE_COLORS: ClassVar = [
        Palette.RUBI_RED,
        Palette.SUNSET_ORANGE,
        Palette.BANANA_YELLOW,
        Palette.BABY_BLUE,
        Palette.OCEAN_BLUE,
    ]
    SCORE_SUP_VALUES: ClassVar = [2.0, 4.0, 6.0, 8.0, 10.0]
    SCORE_INF_VALUES = [0.0] + SCORE_SUP_VALUES[:-1]

    def __init__(self) -> None:
        """Creates template Score Color Discrete Map spec."""
        super().__init__(
            *(
                DiscreteMapIntervalItem(
                    min_value=min_val,
                    max_value=max_val,
                    color=color_val,
                    exclude_min=False,
                    exclude_max=idx < len(self.SCORE_COLORS) - 1,
                )
                for idx, (min_val, max_val, color_val) in enumerate(
                    zip(self.SCORE_INF_VALUES, self.SCORE_SUP_VALUES, self.SCORE_COLORS)
                )
            )
        )
