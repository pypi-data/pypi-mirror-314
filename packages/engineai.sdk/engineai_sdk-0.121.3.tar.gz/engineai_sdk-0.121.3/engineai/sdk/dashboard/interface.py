"""Specs for Layout Package Interfaces."""

from typing import List

from engineai.sdk.dashboard.abstract.layout import AbstractLayoutItem
from engineai.sdk.dashboard.base import DependencyInterface


class CardInterface(AbstractLayoutItem):
    """Specs for Card Interface."""


class CollapsibleInterface(AbstractLayoutItem):
    """Specs for Card Interface."""


class GridInterface(AbstractLayoutItem):
    """Specs for Grid  Interface."""


class SelectableInterface(AbstractLayoutItem):
    """Specs for Selectable Interface."""


class WidgetInterface:
    """Interface for Widget instance."""


class RouteInterface:
    """Specs for Route Interface."""


class OperationInterface:
    """Specs for Operation Interface."""

    _FORCE_SKIP_VALIDATION: bool = False

    @property
    def force_skip_validation(self) -> bool:
        """Returns True if widget height is forced."""
        return self._FORCE_SKIP_VALIDATION

    @property
    def dependencies(self) -> List[DependencyInterface]:
        """Returns operation id."""
        return []


class HttpInterface:
    """Specs for Http Interface."""
