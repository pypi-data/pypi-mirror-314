"""Spec for Discrete color map."""

from typing import Any
from typing import Dict
from typing import List
from typing import Protocol
from typing import Union

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.decorator import type_check

from .palette import Palette
from .single import Single


class DiscreteMapIntervalItem(AbstractFactory):
    """Map value intervals to colors.

    Define specifications for creating a color discrete
    map item, enabling association of a color with an
    interval of numerical values.
    """

    @type_check
    def __init__(
        self,
        *,
        min_value: Union[int, float],
        max_value: Union[int, float],
        color: Union[Palette, Single],
        exclude_min: bool = False,
        exclude_max: bool = False,
    ) -> None:
        """Constructor for DiscreteMapIntervalItem.

        Args:
            min_value: start of the interval.
            max_value: end of the interval.
            color: color applied to interval (Palette)
                or color itself (Single).
            exclude_min: whether to make min exclusive. (Default: ``False``)
            exclude_max: whether to make max exclusive. (Default: ``False``)
        """
        super().__init__()
        self.__color = color if isinstance(color, Single) else Single(color=color)
        self.__min = min_value
        self.__max = max_value
        self.__exclude_min = exclude_min
        self.__exclude_max = exclude_max

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "min": self.__min,
            "max": self.__max,
            "color": self.__color.build(),
            "excludeMax": self.__exclude_max,
            "excludeMin": self.__exclude_min,
        }


class DiscreteMapValueItem(AbstractFactory):
    """Map single values to colors.

    Create a specification to represent a discrete mapping between a
    single value and a specific color within a discrete color map.
    """

    @type_check
    def __init__(
        self,
        value: Union[int, float],
        color: Union[Palette, Single],
    ) -> None:
        """Constructor for DiscreteMapValueItem.

        Args:
            value: value for which the color will be applied.
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


DiscreteMapItem = Union[DiscreteMapIntervalItem, DiscreteMapValueItem]


class DiscreteMap(AbstractFactory):
    """Map values to specific colors.

    Construct a specification for creating a discrete map of colors.
    The DiscreteMap class allows users to define a set of
    DiscreteMapItem objects, each representing a mapping
    between a specific value or category and a corresponding color.
    """

    @type_check
    def __init__(self, *items: DiscreteMapItem) -> None:
        """Constructor for DiscreteMap.

        Args:
            items: list of values, intervals composing the
                color map (DiscreteMapIntervalItem or DiscreteMapValueItem)

        Examples:
            ??? example "Create a discrete color map with DiscreteMapIntervalItem"
                ```py linenums="1"
                import pandas as pd
                from engineai.sdk.dashboard.styling import color
                    color.DiscreteMapValueItem(
                        value=1, color=color.Palette.GRASS_GREEN
                    ),
                    color.DiscreteMapValueItem(value=2, color=color.Palette.BABY_BLUE)
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
                            color_spec=discrete_color,
                            data_column="color",
                        )
                    )
                )
                Dashboard(content=ts)
                ```
        """
        super().__init__()
        self.__items: List[DiscreteMapItem] = list(items)

    @staticmethod
    def __build_item(
        item: DiscreteMapItem,
    ) -> Dict[str, Any]:
        input_key = "value" if isinstance(item, DiscreteMapValueItem) else "interval"

        return {input_key: item.build()}

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "items": [self.__build_item(item) for item in self.__items],
        }


class _ColorMethod(Protocol):
    def __call__(self, *, index: int) -> Palette: ...


def generate_color_mapping(*, length: int, color_method: _ColorMethod) -> DiscreteMap:
    """Generate color mapping by length, method.

    Function to generate a color mapping based on specified
    parameters like length and color method.

    Examples:
        ??? example "Create a discrete color map with DiscreteMapIntervalItem"
            ```py linenums="1"
            from engineai.sdk.dashboard.styling.color.palette import (
                qualitative_palette
            )

            generate_color_mapping(length=2, color_method=qualitative_palette)

            # Result
            DiscreteMap(
                items=[
                    DiscreteMapValueItem(
                        value=1,
                        color=QUALITATIVE_PALETTE_FIRST_COLOR
                    ),
                    DiscreteMapValueItem(
                        value=2,
                        color=QUALITATIVE_PALETTE_SECOND_COLOR
                    ),
                ]
            )
            ```
    """
    items: List[Union[DiscreteMapIntervalItem, DiscreteMapValueItem]] = [
        DiscreteMapValueItem(value=num + 1, color=Single(color=color_method(index=num)))
        for num in range(length)
    ]
    return DiscreteMap(*items)
