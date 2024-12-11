"""Spec for defining dependencies with a widget."""

from typing import Any
from typing import Dict
from typing import Iterator
from typing import Optional
from typing import Tuple

from engineai.sdk.dashboard.base import DependencyInterface


class WidgetSelectDependency(DependencyInterface):
    """Specs base for defining the Widget Dependency."""

    API_DEPENDENCY_INPUT: Optional[str] = None
    _INPUT_KEY = "widget"

    def __init__(
        self, *, dependency_id: str, widget_id: str, path: str = "selected"
    ) -> None:
        """Creates dependency with a widget.

        Args:
            dependency_id: id of dependency (to be used in other dependencies)
            widget_id: id of widget to associate dependency with
            path: path for state exposed by widget
        """
        super().__init__()
        self.__dependency_id = dependency_id
        self.__widget_id = widget_id
        self.__path = path

    def __iter__(self) -> Iterator[Tuple[str, str]]:
        yield "dependency_id", self.__dependency_id
        yield "widget_id", self.__widget_id
        yield "path", self.__path

    def __hash__(self) -> int:
        return hash(tuple(self))

    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and tuple(self) == tuple(other)

    @property
    def api_dependency_input(self) -> str:
        """Return the API input to cast in api types during build."""
        if self.API_DEPENDENCY_INPUT is None:
            msg = f"Class {self.__class__.__name__}.API_DEPENDENCY_INPUT not defined."
            raise NotImplementedError(msg)
        return self.API_DEPENDENCY_INPUT

    @property
    def dependency_id(self) -> str:
        """Return Dependency ID."""
        return self.__dependency_id

    @property
    def widget_id(self) -> str:
        """Returns id of widget associated with WidgetDependency.

        Returns:
            str: widget id
        """
        return self.__widget_id

    @widget_id.setter
    def widget_id(self, widget_id: str) -> None:
        """Change widget_id associated with WidgetDependency."""
        self.__widget_id = widget_id

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Any: Input object for Dashboard API
        """
        return {
            "widgetId": self.__widget_id,
            "path": self.__path,
            "name": self.__dependency_id,
        }
