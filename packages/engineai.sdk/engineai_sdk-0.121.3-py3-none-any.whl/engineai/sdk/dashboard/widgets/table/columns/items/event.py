"""Specification for External Action columns in Table widget."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.widgets.components.actions.links.external import (
    ExternalEvent,
)
from engineai.sdk.dashboard.widgets.table.columns.items.base import Column

Actions = ExternalEvent


class EventColumn(Column):
    """Specifications for EventColumn class."""

    _ITEM_ID_TYPE: str = "EVENT_COLUMN"

    @type_check
    def __init__(
        self,
        *,
        action: Actions,
        label: Optional[Union[str, WidgetField]] = None,
        hiding_priority: int = 0,
        tooltip_text: Optional[List[TemplatedStringItem]] = None,
        min_width: Optional[int] = None,
    ) -> None:
        """Class EventColumn is used as urlx column for the Table Widget.

        Args:
            action: action to be triggered on click.
            label: label to be displayed for this column.
            hiding_priority: columns with lower hiding_priority are hidden first
                if not all data can be shown.
            tooltip_text: info text to explain column. Each element of list is
                displayed as a separate paragraph.
            min_width: min width of the column in pixels.
        """
        super().__init__(
            data_column=action.data_column,
            label=label,
            hiding_priority=hiding_priority,
            tooltip_text=tooltip_text,
            min_width=min_width,
        )
        self.__action = action

    def prepare(self) -> None:
        """Url Column has no styling."""

    def _custom_validation(
        self,
        *,
        data: pd.DataFrame,
    ) -> None:
        """Custom validation for each columns to implement."""
        self.__action.validate(data=data, widget_class="Table")

    def _build_event(self) -> Dict[str, Any]:
        return {
            "actionExternalEventHyperLink": self.__action.build(),
        }

    def _build_column(self) -> Dict[str, Any]:
        return {"actionColumn": {"actions": self._build_event()}}
