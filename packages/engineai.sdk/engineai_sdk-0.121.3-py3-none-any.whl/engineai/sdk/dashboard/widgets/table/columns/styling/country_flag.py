"""Specification for styling a column with a country flag to a value."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links import WidgetField

from .base import TableColumnStylingBase


class CountryFlagStyling(TableColumnStylingBase):
    """Styling options for country flag column.

    Specify the styling options for a country flag column
    in the table widget, including position and data column.
    """

    @type_check
    def __init__(
        self,
        *,
        left: bool = True,
        data_column: Optional[Union[str, WidgetField]] = None,
    ) -> None:
        """Constructor for CountryFlagStyling.

        Args:
            data_column: id of column which values are used to determine behavior of
                arrow.
                By default, will use values of column to which styling is applied.
            left: whether to put flag to the left (True) or right (False) of column
                value.
        """
        super().__init__(data_column=data_column, color_spec=None)
        self.__left = left

    def _build_extra_inputs(self) -> Dict[str, Any]:
        return {"left": self.__left}
