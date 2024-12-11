"""Specification for url columns in Table widget."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.templated_string import DataField
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.widgets.components.actions.links import UrlLink

from .base import Column


class UrlColumn(Column):
    """Specifications for UrlColumn class."""

    _ITEM_ID_TYPE: str = "URL_COLUMN"

    @type_check
    def __init__(
        self,
        *,
        data_column: Union[str, WidgetField],
        url_tooltip: Optional[DataField] = None,
        label: Union[str, WidgetField] = "",
        hiding_priority: int = 0,
        tooltip_text: Optional[List[TemplatedStringItem]] = None,
        min_width: Optional[int] = None,
    ) -> None:
        """Class UrlColumn is used as urlx column for the Table Widget.

        Args:
            data_column: name of column in pandas dataframe(s) used for the url
                information in the Column.
            url_tooltip: fixed or dynamic text for all url rows. Each element of list
                is displayed as a separate paragraph.
            label: label to be displayed for this column.
            hiding_priority: columns with lower hiding_priority are hidden first
                if not all data can be shown.
            tooltip_text: info text to explain column. Each element of list is
                displayed as a separate paragraph.
            min_width: min width of the column in pixels.

        Examples:
            ??? example "Create a Table widget with UrlColumn"
                ```py linenums="1"
                import pandas as pd
                from engineai.sdk.dashboard.dashboard import Dashboard
                from engineai.sdk.dashboard.widgets import table
                data = pd.DataFrame(
                    {
                        "url": "www.apple.com",
                    }
                )
                Dashboard(
                    content=table.Table(
                        data=data,
                        columns=[
                            table.UrlColumn(
                                data_column="url",
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
        )
        self.__url_link = UrlLink(
            data_column=data_column,
            tooltip=url_tooltip,
        )

    def prepare(self) -> None:
        """Url Column has no styling."""

    def _custom_validation(
        self,
        *,
        data: pd.DataFrame,
    ) -> None:
        """Custom validation for each columns to implement.

        Args:
            data: pandas dataframe which will be used for table.

        Raises:
            ValueError: if data does not contain data_column for TableColumn
        """
        self.__url_link.validate(data=data, widget_class="Table")

    def _build_column(self) -> Dict[str, Any]:
        return {
            "actionColumn": {"actions": {"hyperLink": self.__url_link.build()}},
        }
