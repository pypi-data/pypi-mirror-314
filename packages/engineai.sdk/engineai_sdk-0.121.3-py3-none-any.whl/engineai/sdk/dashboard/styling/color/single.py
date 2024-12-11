"""Spec for SingleColor class."""

from typing import Any
from typing import Dict

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.decorator import type_check

from .palette import Palette


class Single(AbstractFactory):
    """Class for creating a single color instance.

    Create a class representing a single color within
    a palette for a Timeseries widget.
    """

    @type_check
    def __init__(self, color: Palette) -> None:
        """Constructor for Single.

        Args:
            color: a color from Palette.
        """
        super().__init__()
        self.__color = color.color

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "customColor": self.__color,
        }
