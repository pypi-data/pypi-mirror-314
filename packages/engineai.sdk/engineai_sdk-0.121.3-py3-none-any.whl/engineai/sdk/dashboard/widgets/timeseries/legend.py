"""Spec for legend of a timeseries widget."""

from typing import Any
from typing import Dict

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.enum.legend_position import LegendPosition


class Legend(AbstractFactory):
    """Spec for legend of a timeseries widget."""

    @type_check
    def __init__(self, *, position: LegendPosition = LegendPosition.BOTTOM) -> None:
        """Construct a legend for a timeseries widget.

        Args:
            position: location of position relative to data, charts.
        """
        super().__init__()
        self.__position = position

    @property
    def position(self) -> LegendPosition:
        """Returns the current Legend Position."""
        return self.__position

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {"position": self.__position.value}
