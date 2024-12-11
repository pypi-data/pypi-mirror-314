"""Specs for WidgetDependencyValue."""

from typing import Any
from typing import Dict

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.links.widget_field import WidgetField


class WidgetDependencyValue(AbstractFactory):
    """Specs for Widget Dependency Value."""

    def __init__(self, widget_field: WidgetField) -> None:
        """Construct for WidgetDependencyValue class.

        Args:
            widget_field (WidgetField): Widget field.
        """
        self.__widget_field = widget_field

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "id": self.__widget_field.link_component.widget_id,
            "state": "selected",
            "path": ["0", self.__widget_field.field],
        }
