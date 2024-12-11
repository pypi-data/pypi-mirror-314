"""Specification for column font styling."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.styling.color.typing import ColorSpec

from .base import TableColumnStylingBase


class FontStyling(TableColumnStylingBase):
    """Font styling options.

    Specify the font styling options for a column in the table widget,
    including color, data column, and background highlighting.
    """

    @type_check
    def __init__(
        self,
        *,
        color_spec: ColorSpec,
        data_column: Optional[Union[str, WidgetField]] = None,
        highlight_background: bool = False,
    ) -> None:
        """Constructor for FontStyling.

        Args:
            data_column: id of column which values are used to determine behavior of
                color of dot. Optional if color_spec is a single color.
            color_spec: spec for color of dot.
            highlight_background: Highlight value background.
        """
        super().__init__(data_column=data_column, color_spec=color_spec)
        self.__highlight_background = highlight_background

    def _build_extra_inputs(self) -> Dict[str, Any]:
        return {"highlightBackground": self.__highlight_background}
