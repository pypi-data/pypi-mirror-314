"""Specs for DashboardRouteLink."""

from typing import Any
from typing import Iterator
from typing import Optional
from typing import Tuple

from engineai.sdk.dashboard.base import AbstractLink
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.dependencies import RouteDependency
from engineai.sdk.dashboard.interface import RouteInterface as Route


class RouteLink(AbstractLink):
    """Establish a link to the route and the widget or layout item."""

    __dependency: Optional[RouteDependency] = None

    @type_check
    def __init__(self, route: Route, field: str) -> None:
        """Construct for DashboardRouteLink class."""
        self.__field = field
        self.__route = route

    def __eq__(self, other: object) -> bool:
        """Return True if other is equal to self."""
        if not isinstance(other, RouteLink):
            return False
        return self.field == other.field and self.link_component == other.link_component

    def __iter__(self) -> Iterator[Tuple[str, str]]:
        yield "field", self.__field

    def __hash__(self) -> int:
        return hash(tuple(self))

    def __repr__(self) -> str:
        return f"R_{next(iter(self.__route.data)).base_path}:{self.__field}"

    @property
    def field(self) -> str:
        """Returns id of field to be used from selectable widget.

        Returns:
            str: field id from selectable widget
        """
        return self.__field

    @property
    def link_component(self) -> Any:
        """Get link route."""
        return self.__route

    @property
    def dependency(self) -> RouteDependency:
        """Return WidgetRouteDependency."""
        if self.__dependency is None:
            self.__dependency = RouteDependency(
                dependency_id="__ROUTE__",
                field=self.__field,
            )
        return self.__dependency

    @property
    def item_id(self) -> str:
        """Return Item Id."""
        return f"ROUTE_{self.__field}"

    def _generate_templated_string(self, *, selection: int = 0) -> str:  # noqa
        """Return the template string to be used in dependency."""
        return f"{{{{__ROUTE__.0.{self.__field}}}}}"
