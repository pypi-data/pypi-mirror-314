"""Specification for staked bar chart columns in Table widget."""

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
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.items.tooltip.stacked_bar import (
    StackedBarTooltip,
)
from engineai.sdk.dashboard.widgets.table.columns.items.exceptions import (
    TableColumnDataColumnNotFoundError,
)
from engineai.sdk.dashboard.widgets.table.columns.styling.stacked_bar import (
    StackedBarStyling,
)

from .base import ChartColumn


class StackedBarColumn(ChartColumn):
    """Define table widget column: Stacked bar chart with data.

    Define a column in the table widget that displays a stacked bar chart,
    including options for data, formatting, styling, and more.
    """

    _ITEM_ID_TYPE: str = "STACKED_BAR"

    @type_check
    def __init__(
        self,
        *,
        data_column: Union[str, WidgetField],
        data_key: Union[str, WidgetField],
        label: Optional[Union[str, GenericLink]] = None,
        bar_label_key: Optional[Union[str, GenericLink]] = None,
        styling: Optional[StackedBarStyling] = None,
        label_key: Optional[str] = None,
        formatting: Optional[NumberFormatting] = None,
        hiding_priority: int = 0,
        tooltip_text: Optional[List[TemplatedStringItem]] = None,
        min_width: Optional[int] = None,
        sortable: bool = True,
        display_total_value: bool = True,
        optional: bool = False,
        tooltip: Optional[StackedBarTooltip] = None,
    ) -> None:
        """Constructor for StackedBarColumn.

        Args:
            data_column: name of column in pandas dataframe(s) used for this widget.
            data_key: key in object that contains the value for the stack bar chart.
            label_key: key in object that contains the label for the stack bar chart.
            label: label to be displayed for this column.
            bar_label_key: key in object that contains the label for the bars.
            formatting: formatting spec.
            styling: styling spec for stacked chart.
            hiding_priority: columns with lower hiding_priority are hidden first
                if not all data can be shown.
            tooltip_text: info text to explain column. Each element of list is
                displayed as a separate paragraph. It will show up as an info icon.
            min_width: min width of the column in pixels.
            sortable: determines if column can be sorted.
            display_total_value: display total value after stacked bars chart.
            optional: flag to make the column optional if there is no Data for that
                columns.
            tooltip: tooltip spec within the stacked bar chart. It will show up once
                the user hovers over the chart.

        Examples:
            ??? example "Create a Table widget with StackedBarColumn"
                ```py linenums="1"
                import pandas as pd
                from engineai.sdk.dashboard.dashboard import Dashboard
                from engineai.sdk.dashboard.widgets import table
                data = pd.DataFrame(
                    {
                        "stacked_data": [
                            {"key": 10, "category": 1},
                            {"key": 10, "category": 2},
                        ],
                    },
                )

                color_spec = color.DiscreteMap(
                        color.DiscreteMapValueItem(
                            value=1, color=color.Palette.MINT_GREEN
                        ),
                        color.DiscreteMapValueItem(
                            value=2, color=color.Palette.SUNSET_ORANGE
                        ),
                    ),
                )

                Dashboard(
                    content=table.Table(
                        data=data,
                        columns=[
                            table.StackedBarColumn(
                                data_column="stacked_data",
                                data_key="key",
                                styling=table.StackedBarStyling(
                                    data_column="category",
                                    color_spec=color_spec,
                            ),
                        ],
                    )
                )
                ```
        """
        super().__init__(
            data_column=data_column,
            data_key=data_key,
            styling=styling,
            label=label,
            hiding_priority=hiding_priority,
            tooltip_text=tooltip_text,
            min_width=min_width,
            reference_line=None,
            optional=optional,
        )
        self.__formatting = formatting if formatting else NumberFormatting()
        self.__sortable = sortable
        self.__display_total_value = display_total_value
        self.__label_key = label_key
        self.__tooltip = tooltip
        self.__bar_label_key = bar_label_key

    def _custom_validation(self, *, data: pd.DataFrame) -> None:
        """Custom validation for each columns to implement.

        Args:
            data: pandas dataframe which will be used for table.
        """
        super()._custom_validation(data=data)

        if isinstance(self.data_column, str):
            if isinstance(self.__bar_label_key, str):
                self.__validate_key(
                    data=data[[self.data_column]],
                    column=self.__bar_label_key,
                    column_name="bar_label_key",
                )
            if isinstance(self.__label_key, str):
                self.__validate_key(
                    data=data[[self.data_column]],
                    column=self.__label_key,
                    column_name="label_key",
                )

    def __validate_key(
        self,
        data: pd.DataFrame,
        column: str,
        column_name: str,
    ) -> None:
        data_to_numpy = data[self.data_column].to_numpy()
        for index in range(len(data_to_numpy)):
            key_data = data_to_numpy[index]
            for element in key_data:
                if column not in element:
                    raise TableColumnDataColumnNotFoundError(
                        column_name=column_name,
                        column_value=column,
                    )

    def _build_column(self) -> Dict[str, Any]:
        return {
            "stackedBarColumn": {
                "formatting": self.__formatting.build(),
                "styling": self._build_styling(),
                "valueKey": build_templated_strings(items=self.data_key),
                "labelKey": build_templated_strings(items=self.__label_key),
                "sortable": self.__sortable,
                "displayTotalValue": self.__display_total_value,
                "optional": self._optional,
                "barLabelKey": (
                    build_templated_strings(items=self.__bar_label_key)
                    if self.__bar_label_key
                    else None
                ),
                "tooltip": self.__tooltip.build() if self.__tooltip else None,
            }
        }
