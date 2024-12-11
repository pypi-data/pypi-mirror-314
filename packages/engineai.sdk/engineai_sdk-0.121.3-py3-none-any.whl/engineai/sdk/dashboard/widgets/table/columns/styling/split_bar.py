"""Specification for styling a column with a split color bar."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.styling import color
from engineai.sdk.dashboard.styling.color.spec import build_color_spec
from engineai.sdk.dashboard.styling.color.typing import ColorSpec

from .base import TableColumnStylingBase
from .exceptions import TableColumnStylingMinMaxValueError


class SplitBarStyling(TableColumnStylingBase):
    """Styling options for split color bar column.

    Specify the styling options for a split color bar column in the
    table widget, including color, data column, min/max values,
    and percentage fill.
    """

    @type_check
    def __init__(
        self,
        *,
        data_column: Optional[Union[str, WidgetField]] = None,
        color_spec: Optional[ColorSpec] = None,
        min_value: Optional[Union[int, float]] = None,
        max_value: Optional[Union[int, float]] = None,
        percentage_fill: float = 0.9,
    ) -> None:
        """Constructor for SplitBarStyling.

        Args:
            data_column: id of column which values are used to determine behavior of
                arrow.
                By default, will use values of column to which styling is applied.
            color_spec: spec for color class.
            min_value: value that determines a 0% bar. By default, takes the minimum
                value in the data.
            max_value: value that determines a full bar. By default, takes the maximum
                value in the data.
            percentage_fill: how much of the cell should the color fill.
        """
        super().__init__(data_column=data_column, color_spec=None)
        if min_value and max_value and min_value >= max_value:
            raise TableColumnStylingMinMaxValueError(
                _class=self.__class__.__name__, min_value=min_value, max_value=max_value
            )
        self.__min_value = min_value
        self.__max_value = max_value
        self.__percentage_fill = percentage_fill
        self.__color_spec = color_spec

    def _build_extra_inputs(self) -> Dict[str, Any]:
        return {
            "min": self.__min_value,
            "max": self.__max_value,
            "mid": 0,
            "percentageFill": self.__percentage_fill,
        }

    def _build_color_spec(self) -> Dict[str, Any]:
        return {
            "colorSpec": build_color_spec(
                spec=self.__color_spec or color.PositiveNegativeDiscreteMap()
            )
        }
