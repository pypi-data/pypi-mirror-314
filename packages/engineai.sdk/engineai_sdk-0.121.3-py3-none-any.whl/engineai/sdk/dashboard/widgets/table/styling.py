"""Spec for Table widget styling."""

from typing import Any
from typing import Dict

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.decorator import type_check


class TableStyling(AbstractFactory):
    """Visual styling options for table widget.

    Specify the visual styling options for the table widget,
    including borders, column lines, row lines, and row height.
    """

    @type_check
    def __init__(
        self,
        *,
        has_borders: bool = True,
        has_column_lines: bool = True,
        has_body_column_lines: bool = True,
        has_row_lines: bool = True,
        single_height_row: bool = True,
    ) -> None:
        """Constructor for TableStyling.

        Args:
            has_borders: whether the outer border of the table are shown.
            has_column_lines: whether vertical lines that separate columns are visible.
            has_body_column_lines: whether vertical lines that separate body columns
                are visible.
            has_row_lines: whether horizontal lines that separate rows are
                visible.
            single_height_row: whether row has single height (True) or double height
                (False).
        """
        super().__init__()
        self.__has_borders = has_borders
        self.__has_column_lines = has_column_lines
        self.__has_body_column_lines = has_body_column_lines
        self.__has_row_lines = has_row_lines
        self.__single_height_row = single_height_row

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "hasBorders": self.__has_borders,
            "hasColumnLines": self.__has_column_lines,
            "hasBodyColumnLines": self.__has_body_column_lines,
            "hasRowLines": self.__has_row_lines,
            "rowHeightSize": "SINGLE" if self.__single_height_row else "DOUBLE",
        }
