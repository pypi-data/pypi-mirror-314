"""Spec for Color Divergent class."""

from typing import Any
from typing import Dict

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.styling.color.palette import Palette
from engineai.sdk.dashboard.styling.color.spec import ColorSpec
from engineai.sdk.dashboard.styling.color.spec import build_color_spec

from .single import Single


class Divergent(AbstractFactory):
    """Creates a class for a Color Divergent."""

    @type_check
    def __init__(
        self,
        mid_value: int,
        mid_color: Palette,
        above_color: ColorSpec,
        below_color: ColorSpec,
    ) -> None:
        """Constructor for ColorDivergent.

        Args:
            mid_value: intermediate value for comparison.
            mid_color: color for intermediate
                value.
            above_color: color spec for value above mid_value.
            below_color: color spec for value below mid_value.
        """
        super().__init__()
        self.__mid_value = mid_value
        self.__mid_color = Single(color=mid_color)
        self.__above_color = above_color
        self.__below_color = below_color

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "midValue": self.__mid_value,
            "midColor": self.__mid_color.build(),
            "aboveColor": build_color_spec(self.__above_color),
            "belowColor": build_color_spec(self.__below_color),
        }
