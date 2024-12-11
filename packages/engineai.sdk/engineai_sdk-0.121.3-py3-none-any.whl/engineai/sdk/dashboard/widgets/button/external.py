"""Spec for Button Action."""

from typing import Any
from typing import Dict

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links.abstract import AbstractFactoryLinkItemsHandler
from engineai.sdk.dashboard.links.widget_field import WidgetField
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.utils import build_data


class ExternalAction(AbstractFactoryLinkItemsHandler):
    """Spec for Button Action."""

    @type_check
    def __init__(
        self,
        *,
        event_type: TemplatedStringItem,
        event_data: WidgetField,
    ) -> None:
        """Construct spec for Button Action.

        Args:
            event_type: event type spec.
            event_data: event data spec.
        """
        super().__init__()
        self.__event_type = event_type
        self.__event_data = event_data

    @property
    def event_type(self) -> TemplatedStringItem:
        """Event type spec."""
        return self.__event_type

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "type": build_templated_strings(items=self.__event_type),
            "data": build_data(
                f"{self.__event_data.dependency.dependency_id}.0."
                f"{self.__event_data.field}"
            ),
        }
