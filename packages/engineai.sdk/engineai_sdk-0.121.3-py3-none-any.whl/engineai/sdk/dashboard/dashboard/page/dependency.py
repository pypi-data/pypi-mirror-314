"""Specs for Dashboard Route Datastore Dependency."""

from typing import Any
from typing import Dict

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.decorator import type_check


class RouteDatastoreDependency(AbstractFactory):
    """Specs for Dashboard Route Datastore Dependency."""

    _INPUT_KEY: str = "urlQuery"

    @type_check
    def __init__(
        self,
        *,
        dependency_id: str,
        query_parameter: str,
    ) -> None:
        """Construct for RouteDatastoreDependency class.

        Args:
            dependency_id: Dependency ID.
            path: Datastore path.
            query_parameter: query parameter to select the series.
        """
        self.__dependency_id = dependency_id
        self.__query_parameter = query_parameter

    @property
    def input_key(self) -> str:
        """Input Key."""
        return self._INPUT_KEY

    @property
    def dependency_id(self) -> str:
        """Returns dependency id.

        Returns:
            str: dependency
        """
        return self.__dependency_id

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "name": self.__dependency_id,
            "query": self.__query_parameter,
        }
