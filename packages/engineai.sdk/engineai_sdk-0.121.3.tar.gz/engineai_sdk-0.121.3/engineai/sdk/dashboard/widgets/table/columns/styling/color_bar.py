"""Specification for styling a column with a color bar."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.styling.color.typing import ColorSpec

from .base import TableColumnStylingBase
from .exceptions import TableColumnStylingMinMaxValueError


class ColorBarStyling(TableColumnStylingBase):
    """Styling options for split color bar column.

    Specify the styling options for a color bar column in the
    table widget, including color, data column, direction,
    min/max values, and percentage fill.
    """

    @type_check
    def __init__(
        self,
        *,
        color_spec: ColorSpec,
        data_column: Optional[Union[str, WidgetField]] = None,
        left_to_right: bool = True,
        min_value: Optional[Union[int, float]] = None,
        max_value: Optional[Union[int, float]] = None,
        percentage_fill: float = 0.9,
    ) -> None:
        """Constructor for ColorBarStyling.

        Args:
            color_spec: spec for bar color.
            data_column: id of column which values are used to determine behavior of
                arrow. By default, will use values of column to which styling is
                applied.
            left_to_right: determines the direction of color bar.
            min_value: value that determines a 0% bar. By default, takes the minimum
                value in the data.
            max_value: value that determines a full bar. By default,
                takes the maximum value in the data.
            percentage_fill: how much of the cell should the color fill.
        """
        super().__init__(color_spec=color_spec, data_column=data_column)

        if min_value and max_value and min_value >= max_value:
            raise TableColumnStylingMinMaxValueError(
                _class=self.__class__.__name__, min_value=min_value, max_value=max_value
            )
        self.__left_to_right = left_to_right
        self.__min_value = min_value
        self.__max_value = max_value
        self.__percentage_fill = percentage_fill

    def _build_extra_inputs(self) -> Dict[str, Any]:
        return {
            "leftToRight": self.__left_to_right,
            "min": self.__min_value,
            "max": self.__max_value,
            "percentageFill": self.__percentage_fill,
        }
