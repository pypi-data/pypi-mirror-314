"""Specification for range columns in Table widget."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting import NumberFormatting
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.links.typing import GenericLink
from engineai.sdk.dashboard.styling import color
from engineai.sdk.dashboard.styling.color import Palette
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.widgets.table.columns.styling.range import RangeStyling

from .base import Column
from .exceptions import TableColumnDataTypeError
from .exceptions import TableRangeColumnValueError


class RangeColumn(Column):
    """Define table widget column: Range values with data source.

    Define a column in the table widget that represents a range of values,
    including options for data source, label, formatting, and styling.
    """

    _ITEM_ID_TYPE: str = "RANGE"

    @type_check
    def __init__(
        self,
        *,
        data_column: Union[str, WidgetField],
        label: Optional[Union[str, GenericLink]] = None,
        formatting: Optional[NumberFormatting] = None,
        styling: Optional[Union[Palette, RangeStyling]] = None,
        hiding_priority: int = 0,
        tooltip_text: Optional[List[TemplatedStringItem]] = None,
        min_width: Optional[int] = None,
        sortable: bool = True,
        optional: bool = False,
    ) -> None:
        """Constructor for RangeColumn.

        Args:
            data_column: name of column in pandas dataframe(s) used for this widget.
            label: label to be displayed for this column.
            formatting: formatting spec.
            styling: styling spec for range.
            hiding_priority: columns with lower hiding_priority are hidden first
                if not all data can be shown.
            tooltip_text: info text to explain column. Each element of list is
                displayed as a separate paragraph.
            min_width: min width of the column in pixels.
            sortable: determines if column can be sorted.
            optional: flag to make the column optional if there is no Data
                for that columns.

        Examples:
            ??? example "Create a Table widget with RangeColumn"
                ```py linenums="1"
                import pandas as pd
                from engineai.sdk.dashboard.dashboard import Dashboard
                from engineai.sdk.dashboard.widgets import table
                data = pd.DataFrame(
                    {
                        "range": [
                            {
                                "min": -10,
                                "value": 0,
                                "max": 10,
                            }
                        ],
                    },
                )
                Dashboard(
                    content=table.Table(
                        data=data,
                        columns=[
                            table.RangeColumn(
                                data_column="range",
                                ),
                            ),
                        ],
                    )
                )
                ```
        """
        super().__init__(
            data_column=data_column,
            label=label,
            hiding_priority=hiding_priority,
            tooltip_text=tooltip_text,
            min_width=min_width,
            optional=optional,
        )
        self.__styling = (
            styling
            if isinstance(styling, RangeStyling)
            else (
                RangeStyling(color_spec=styling)
                if isinstance(styling, Palette)
                else RangeStyling(
                    color_spec=color.Single(color=color.Palette.MINT_GREEN)
                )
            )
        )
        self.__sortable = sortable
        self.__formatting = formatting if formatting else NumberFormatting()

    def prepare(self) -> None:
        """Prepare data column."""
        if self.__styling:
            self.__styling.prepare(self._data_column)

    def _custom_validation(self, *, data: pd.DataFrame) -> None:
        """Custom validation for each columns to implement.

        Args:
            data: pandas dataframe which will be used for table.
        """
        if isinstance(self.data_column, str):
            data_to_numpy = data[self.data_column].to_numpy()
            for index in range(len(data_to_numpy)):
                element = data_to_numpy[index]
                if not isinstance(element, dict):
                    raise TableColumnDataTypeError(
                        data_column=self.data_column,
                        row_type=type(element),
                        types="Dict",
                    )
                for field in ["min", "value", "max"]:
                    if field not in element:
                        raise TableRangeColumnValueError(
                            data_column=self.data_column, key=field
                        )
        if self.__styling:
            self.__styling.validate(data=data)

    def _build_column(self) -> Dict[str, Any]:
        return {
            "rangeColumn": {
                "formatting": self.__formatting.build(),
                "styling": self.__styling.build(),
                "sortable": self.__sortable,
                "optional": self._optional,
            }
        }
