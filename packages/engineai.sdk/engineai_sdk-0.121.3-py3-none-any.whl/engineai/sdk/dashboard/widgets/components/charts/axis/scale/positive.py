"""Spec for scale for y axis with only positive values."""

from typing import Any
from typing import Dict
from typing import Optional

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.decorator import type_check


class AxisScalePositive(AbstractFactory):
    """Y-axis scale for charts with positive values.

    Construct specifications for a scale for the y-axis with only
    positive values. It assumes the minimum value of the chart to be
    fixed at 0. Specify a fixed maximum value for the axis with the
    max_value parameter, which defaults to None, allowing for
    dynamic calculation of the maximum value.
    """

    @type_check
    def __init__(
        self, *, max_value: Optional[int] = None, intermediate_tick_amount: int = 3
    ) -> None:
        """Constructor for AxisScalePositive.

        Args:
            max_value: fixed maximum value for axis.
                Defaults to None (max value calculated dynamically)
            intermediate_tick_amount: number of extra ticks between extremes.
        """
        super().__init__()
        self.__max_value = max_value
        self.__intermediate_tick_amount = intermediate_tick_amount

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "max": self.__build_max_value(),
            "tickAmount": self.__intermediate_tick_amount,
        }

    def __build_max_value(
        self,
    ) -> Dict[str, Any]:
        return {
            "max": self.__max_value,
        }
