"""Specification for styling a column with an arrow next to value."""

import enum
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.styling.color.typing import ColorSpec

from .base import TableColumnStylingBase


class RangeShape(enum.Enum):
    """Range shape options."""

    CIRCLE = "CIRCLE"
    RECTANGLE = "RECTANGLE"


class RangeStyling(TableColumnStylingBase):
    """Styling options for range column.

    Specify the styling options for a range column in the
    table widget, including color, data column, and shape.
    """

    @type_check
    def __init__(
        self,
        *,
        color_spec: ColorSpec,
        data_column: Optional[Union[str, WidgetField]] = None,
        shape: RangeShape = RangeShape.CIRCLE,
    ) -> None:
        """Constructor for RangeStyling.

        Args:
            data_column: id of column which values are used to determine behavior of
                arrow.
            color_spec: spec for color of range value.
            shape: shape of range indicator.
        """
        super().__init__(
            data_column=data_column,
            color_spec=color_spec,
        )
        self.__shape = shape

    def _build_extra_inputs(self) -> Dict[str, Any]:
        return {"shape": self.__shape.value}
