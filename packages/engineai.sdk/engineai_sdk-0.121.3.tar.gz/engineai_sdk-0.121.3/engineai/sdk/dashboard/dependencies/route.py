"""Spec for defining a dependency with a widget."""

from typing import Any
from typing import Dict
from typing import Iterator
from typing import Optional
from typing import Tuple

from engineai.sdk.dashboard.base import DependencyInterface


class RouteDependency(DependencyInterface):
    """Spec for defining a dependency with a datastore."""

    API_DEPENDENCY_INPUT: Optional[str] = None
    _INPUT_KEY = "dashboardPage"

    def __init__(self, *, dependency_id: str, field: str) -> None:
        """Creates dependency with a series in a datastore.

        Args:
            dependency_id (str): id of dependency (to be used in other dependencies)
            field (str): field ID inside the datastore.
        """
        self.__dependency_id = dependency_id
        self.__field_id = field

    def __iter__(self) -> Iterator[Tuple[str, str]]:
        yield "field_id", self.__field_id

    def __hash__(self) -> int:
        return hash(self.__dependency_id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and (
            self.dependency_id == other.dependency_id
        )

    @property
    def api_dependency_input(self) -> str:
        """Return the API input to cast in api types during build."""
        if self.API_DEPENDENCY_INPUT is None:
            msg = f"Class {self.__class__.__name__}.API_DEPENDENCY_INPUT not defined."
            raise NotImplementedError(msg)
        return self.API_DEPENDENCY_INPUT

    @property
    def dependency_id(self) -> str:
        """Get Dependency ID."""
        return self.__dependency_id

    @property
    def field_id(self) -> str:
        """Get Field ID."""
        return self.__field_id

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Any: Input object for Dashboard API
        """
        return {
            "name": self.__dependency_id,
        }
