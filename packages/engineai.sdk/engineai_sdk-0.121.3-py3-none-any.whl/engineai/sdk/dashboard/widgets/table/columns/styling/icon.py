"""Specification for styling a column with an icon to a value."""

from typing import Any
from typing import Dict
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links import WidgetField

from .base import TableColumnStylingBase


class IconStyling(TableColumnStylingBase):
    """Styling options for icon column.

    Specify the styling options for an icon column in the
    table widget, including data column and position.
    """

    @type_check
    def __init__(
        self,
        *,
        data_column: Union[str, WidgetField],
        left: bool = True,
    ) -> None:
        """Constructor for IconStyling.

        Args:
            data_column: id of column which values are used to determine behavior of
                arrow.
                By default, will use values of column to which styling is applied.
            left: whether to put icon to the left (True) or right (False) of column
                value.
        """
        super().__init__(data_column=data_column, color_spec=None)
        self.__left = left

    def _build_extra_inputs(self) -> Dict[str, Any]:
        return {"left": self.__left}
