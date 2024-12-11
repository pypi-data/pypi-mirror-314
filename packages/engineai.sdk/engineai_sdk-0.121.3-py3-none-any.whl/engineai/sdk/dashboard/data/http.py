"""Spec for defining data from a http request."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from engineai.sdk.dashboard.dependencies.http import HttpDependency
from engineai.sdk.dashboard.dependencies.http import HttpHeader
from engineai.sdk.dashboard.interface import HttpInterface
from engineai.sdk.dashboard.interface import OperationInterface as OperationItem
from engineai.sdk.dashboard.links.abstract import AbstractFactoryLinkItemsHandler
from engineai.sdk.dashboard.templated_string import TemplatedStringItem


class Http(AbstractFactoryLinkItemsHandler, HttpInterface):
    """Spec for defining data from a http request."""

    def __init__(
        self,
        *,
        path: TemplatedStringItem,
        host: str,
        headers: Optional[Dict[str, str]] = None,
        operations: Optional[List[OperationItem]] = None,
    ) -> None:
        """Constructor for Http class.

        Args:
            path: path to the data.
            host: host of the data.
            headers: headers for the request.
            operations: operations to be performed on the data.
        """
        super().__init__()
        self.__path = path
        self.__dependency = HttpDependency(
            path=self.__path,
            host=host,
            headers=(
                [HttpHeader(key=key, value=value) for key, value in headers.items()]
                if headers is not None
                else None
            ),
            operations=operations,
        )

    @property
    def base_path(self) -> str:
        """Return the base path."""
        return "http"

    @property
    def separator(self) -> str:
        """Return the separator."""
        return "/"

    @property
    def dependency(self) -> HttpDependency:
        """Property to get the dependency object."""
        return self.__dependency

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return self.__dependency.build()
