"""Spec for Button Action."""

from typing import Any
from typing import Dict
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.actions.links.base import BaseLink


class ExternalEvent(BaseLink):
    """Spec for External Event Action."""

    _INPUT_KEY: str = "actionExternalEventHyperLink"

    @type_check
    def __init__(
        self,
        *,
        event_type: TemplatedStringItem,
        data_column: Union[str, WidgetField],
    ) -> None:
        """Construct spec for ExternalEvent.

        Args:
            event_type: event type spec.
            data_column: event data spec.
        """
        super().__init__(data_column=data_column)
        self.__event_type = event_type

    @property
    def data_column(self) -> Union[str, WidgetField]:
        """Get data column."""
        return self._data_column

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API."""
        return {
            "type": build_templated_strings(items=self.__event_type),
            "dataKey": build_templated_strings(items=self._data_column),
        }
