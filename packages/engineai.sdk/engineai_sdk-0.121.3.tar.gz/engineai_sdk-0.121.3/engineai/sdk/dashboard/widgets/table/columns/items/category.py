"""Specification for Category Columns in Table widget."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting import MapperFormatting
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.links.typing import GenericLink
from engineai.sdk.dashboard.styling.color import Palette
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.widgets.table.columns.items.exceptions import (
    TableCategoryColumnMappingError,
)
from engineai.sdk.dashboard.widgets.table.columns.styling.cell import CellStyling
from engineai.sdk.dashboard.widgets.table.columns.styling.country_flag import (
    CountryFlagStyling,
)
from engineai.sdk.dashboard.widgets.table.columns.styling.dot import DotStyling
from engineai.sdk.dashboard.widgets.table.columns.styling.font import FontStyling
from engineai.sdk.dashboard.widgets.table.columns.styling.utils import (
    build_styling_input,
)
from engineai.sdk.dashboard.widgets.table.enums import HorizontalAlignment

from .base import Column

CategoryColumnStyling = Union[
    CellStyling,
    CountryFlagStyling,
    DotStyling,
    FontStyling,
]


class CategoryColumn(Column):
    """Define table widget column: Categorize data with source.

    Define a column in the table widget that categorizes data, with
    options for data source, label, formatting, styling, and alignment.
    """

    _ITEM_ID_TYPE: str = "CATEGORY"

    @type_check
    def __init__(
        self,
        *,
        data_column: Union[str, WidgetField],
        label: Optional[Union[str, GenericLink]] = None,
        formatting: MapperFormatting,
        styling: Optional[Union[Palette, CategoryColumnStyling]] = None,
        align: HorizontalAlignment = HorizontalAlignment.LEFT,
        hiding_priority: int = 0,
        tooltip_text: Optional[List[TemplatedStringItem]] = None,
        min_width: Optional[int] = None,
        sortable: bool = False,
        optional: bool = False,
    ) -> None:
        """Constructor for CategoryColumn.

        Args:
            data_column: name of column in pandas dataframe(s) used for this widget.
            label: label to be displayed for this column.
            formatting: formatting spec.
            styling: styling spec for column. One of TableColumnStylingCell,
                TableColumnStylingCountryFlag or TableColumnStylingDot.
            align: column align.
            hiding_priority: columns with lower hiding_priority are hidden first
                if not all data can be shown.
            tooltip_text: info text to explain column. Each element of list is
                displayed as a separate paragraph.
            min_width: min width of the column in pixels.
            sortable: determines if column can be sorted.
            optional: flag to make the column optional if there is no Data for that
                columns.

        Examples:
            ??? example "Create a Table widget with CategoryColumn"
                ```py linenums="1"
                import pandas as pd
                from engineai.sdk.dashboard.dashboard import Dashboard
                from engineai.sdk.dashboard.widgets import table
                data = pd.DataFrame(
                    {
                        "category": [3, 2, 3, 1],
                    },
                )
                Dashboard(
                    content=table.Table(
                        data=data,
                        columns=[
                            table.CategoryColumn(
                                data_column="category",
                                formatting=MapperFormatting(mapping={
                                        1: "Low", 2: "Mid", 3: "High"
                                    }
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
        self.__align = align
        self.__styling = (
            CellStyling(color_spec=styling) if isinstance(styling, Palette) else styling
        )
        self.__sortable = sortable
        self.__formatting = formatting

    def prepare(self) -> None:
        """Prepare data column."""
        if self.__styling is not None:
            self.__styling.prepare(self._data_column)

    def _custom_validation(self, *, data: pd.DataFrame) -> None:
        """Custom validation for each columns to implement.

        Args:
            data: pandas dataframe which will be used for table.

        Raises:
            TableCategoryColumnMappingError: if data does not contain data_column
                for TableColumn
        """
        if self.__styling:
            self.__styling.validate(data=data)

        unique_values = set(data[data[self.data_column].notna()][self.data_column])
        formatting_keys = set(self.__formatting.mapping.keys())
        missing_formatting = unique_values.difference(formatting_keys)

        if len(missing_formatting) > 0:
            raise TableCategoryColumnMappingError(
                missing_formatting=missing_formatting,
                data_column=self.data_column,
            )

    def _build_styling(self) -> Dict[str, Any]:
        return (
            None
            if self.__styling is None
            else build_styling_input(
                data_column=self.data_column, styling=self.__styling
            )
        )

    def _build_column(self) -> Dict[str, Any]:
        return {
            "categoryColumn": {
                "sortable": self.__sortable,
                "formatting": self.__formatting.build(),
                "align": self.__align.value,
                "styling": self._build_styling(),
                "optional": self._optional,
            }
        }
