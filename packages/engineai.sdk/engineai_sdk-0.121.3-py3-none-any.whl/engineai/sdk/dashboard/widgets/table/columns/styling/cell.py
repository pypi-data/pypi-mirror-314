"""Specification for styling a column with an arrow next to value."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.styling.color.typing import ColorSpec

from .base import TableColumnStylingBase


class CellStyling(TableColumnStylingBase):
    """Styling options for table widget cell.

    Specify the styling options for a cell in the table widget,
    including color, data column, and percentage fill.
    """

    @type_check
    def __init__(
        self,
        *,
        color_spec: ColorSpec,
        data_column: Optional[Union[str, WidgetField]] = None,
        percentage_fill: Optional[Union[int, float]] = 1,
    ) -> None:
        """Constructor for CellStyling.

        Args:
            data_column: id of column which values are used to determine behavior of
                arrow. By default, will use values of column to which styling is
                applied.
            percentage_fill: how much of the cell should the color
                fill. Default to 1, meaning the whole cell
            color_spec: spec for color of arrows.
        """
        super().__init__(color_spec=color_spec, data_column=data_column)
        self.__percentage_fill = percentage_fill

    def _build_extra_inputs(self) -> Dict[str, Any]:
        return {"percentageFill": self.__percentage_fill}
