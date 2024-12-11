"""Spec for Gradients."""

from typing import Any
from typing import Dict
from typing import Union

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.styling.color.palette import Palette

from .single import Single


class GradientItem(AbstractFactory):
    """Represents value and corresponding color in a gradient.

    Item within a color gradient, representing a value and its
    corresponding color. For instance suppose that a gradient has
    3 colors, the Gradient class will have 3 GradientItem(s).
    """

    @type_check
    def __init__(
        self,
        *,
        value: Union[int, float],
        color: Union[Palette, Single],
    ) -> None:
        """Constructor for GradientItem.

        Args:
            value: initial value of interval with color.
            color: color applied to interval (Palette)
                or color itself (Single).
        """
        super().__init__()
        self.__color = color if isinstance(color, Single) else Single(color=color)
        self.__value = value

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {"color": self.__color.build(), "value": self.__value}


class Gradient(AbstractFactory):
    """Define gradient for smooth transitions between colors.

    Create a specification for defining a color gradient, allowing
    for smooth transitions between colors. The Gradient class
    facilitates the creation of a continuous range of colors by
    specifying a set of GradientItem objects representing key
    points along the gradient.
    """

    @type_check
    def __init__(self, *items: GradientItem, steps: int = 10) -> None:
        """Constructor for Gradient.

        Args:
            items: map between color and intervals.
            steps: number of intermediate colors between gradient items.
                Defaults to 10.

        Examples:
            ??? example "Create a gradient with 3 colors"
                ```py linenums="1"
                import pandas as pd
                from engineai.sdk.dashboard.styling import color
                from engineai.sdk.dashboard.widgets import timeseries
                from engineai.sdk.dashboard.dashboard import Dashboard
                # Create the color schema
                gradient_color = color.Gradient(
                    color.GradientItem(value=0, color=color.Palette.RUBI_RED),
                    color.GradientItem(value=2.5, color=color.Palette.GRASS_GREEN),
                    color.GradientItem(value=5, color=color.Palette.BABY_BLUE)
                )
                # Create the timeseries and apply the color schema
                data = pd.DataFrame(
                    {
                        "value": [10, 20, 30, 10, 20, 30, 10, 20, 30, 10],
                        "color": [0, 1, 2, 0, 1, 2, 0, 1, 2, 0],
                    },
                    index=pd.date_range("2020-01-01", "2020-01-10"),
                )
                ts = timeseries.Timeseries(
                    data
                ).set_series(
                    timeseries.LineSeries(
                        data_column="value",
                        styling=timeseries.LineSeriesStyling(
                            color_spec=gradient_color,
                            data_column="color",
                        )
                    )
                )
                Dashboard(content=ts)
                ```
        """
        super().__init__()
        self.__items = items
        self.__steps = steps

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "colorMap": [item.build() for item in self.__items],
            "nSteps": self.__steps,
        }
