"""Specs for dashboard Route."""

from typing import Any
from typing import Dict
from typing import List
from typing import Union

import pandas as pd
from typing_extensions import Unpack

from engineai.sdk.dashboard.abstract.typing import PrepareParams
from engineai.sdk.dashboard.dashboard.page.dependency import RouteDatastoreDependency
from engineai.sdk.dashboard.data.manager.manager import DependencyManager
from engineai.sdk.dashboard.data.manager.manager import RouteDataType
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.interface import DependencyInterface
from engineai.sdk.dashboard.interface import RouteInterface
from engineai.sdk.dashboard.links import RouteLink
from engineai.sdk.dashboard.selected import Selected


class _Selected(Selected["Route", RouteLink, "Route"]):
    """Route Selected property configuration."""


class Route(DependencyManager, RouteInterface):
    """Specs for dashboard Route."""

    _DEPENDENCY_ID = "__ROUTE__"

    @type_check
    def __init__(
        self,
        data: RouteDataType,
        *,
        query_parameter: str,
    ) -> None:
        """Constructor for dashboard Route.

        Args:
            data: data for the widget. Can be a
                pandas dataframe or Storage object if the data is to be retrieved
                from a storage.
            query_parameter: parameter that will be used to apply url queries.
        """
        super().__init__(data=data, base_path="route")
        self.__query_parameter = query_parameter
        self.__dependency: RouteDatastoreDependency = RouteDatastoreDependency(
            query_parameter=query_parameter,
            dependency_id=f"{self.dependency_id}{query_parameter}",
        )
        self.selected = _Selected(component=self)
        self._route_data_dependency: DependencyInterface

    @property
    def data_id(self) -> str:
        """Returns data id."""
        return "route"

    @property
    def query_parameter(self) -> str:
        """Query parameter."""
        return self.__query_parameter

    def prepare(self, **kwargs: Unpack[PrepareParams]) -> None:
        """Prepare page routing."""
        self._prepare_dependencies(**kwargs)
        # Will always be one dependency
        if not hasattr(self, "_route_data_dependency"):
            self._route_data_dependency = next(iter(self.dependencies))
            self._route_data_dependency.prepare(self.__dependency.dependency_id)

    def validate(self, data: pd.DataFrame, **_: Any) -> None:
        """Page routing has no validations to do."""

    @property
    def dependency(self) -> List[Union[RouteDatastoreDependency, DependencyInterface]]:
        """Returns dependency."""
        return [self.__dependency, self._route_data_dependency]

    def build(self) -> Dict[str, Any]:
        """Build Item."""
        # TODO: Need to validate if we can remove this method.
