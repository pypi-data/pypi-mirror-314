"""Spec for defining a dependency with a widget."""

from typing import Any
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from engineai.sdk.dashboard.base import DependencyInterface
from engineai.sdk.dashboard.interface import OperationInterface as OperationItem
from engineai.sdk.dashboard.templated_string import build_templated_strings


class BaseStorage(DependencyInterface):
    """Spec for defining a dependency with a datastore."""

    def __init__(
        self,
        *,
        dependency_id: str,
        series_id: str,
        operations: Optional[List[OperationItem]] = None,
    ) -> None:
        """Creates dependency with a series in a datastore.

        Args:
            dependency_id: id of dependency (to be used in other dependencies)
            series_id: id of series in datastore.
                Defaults to empty string.
            operations: list of operations to be applied to data.
        """
        super().__init__()
        self.__dependency_id = dependency_id
        self.__series_id = series_id
        self.__operations = operations or []

    def __iter__(self) -> Iterator[Tuple[str, str]]:
        yield "dependency_id", self.__dependency_id
        yield "series_id", self.__series_id

    def __hash__(self) -> int:
        return hash(f"{self.__dependency_id}_{self.__series_id}")

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, type(self))
            and self.__series_id == other.series_id
            and self.__dependency_id == other.dependency_id
        )

    @property
    def dependency_id(self) -> str:
        """Returns dependency id.

        Returns:
            str: dependency
        """
        return self.__dependency_id

    @property
    def series_id(self) -> str:
        """Returns series id.

        Returns:
            str: series id
        """
        return self.__series_id

    def prepare(self, route_dependency_id: str) -> None:
        """Prepare dependency."""
        if len(route_dependency_id) > 0:
            self.__series_id = f"{self.__series_id}/{{{{{route_dependency_id}}}}}"

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Any: Input object for Dashboard API
        """
        return {
            "fileName": build_templated_strings(items=self.__series_id),
            "name": self.__dependency_id,
            "operations": [operation.build() for operation in self.__operations],
        }


class DashboardBlobStorage(BaseStorage):
    """Spec for defining a dependency with a datastore."""

    _INPUT_KEY = "dashboardSelfBlobStore"


class DashboardFileShareStorage(BaseStorage):
    """Spec for defining a dependency with a datastore."""

    _INPUT_KEY = "azureFileShareSelfStorage"


DashboardStorage = Union[DashboardBlobStorage, DashboardFileShareStorage]
