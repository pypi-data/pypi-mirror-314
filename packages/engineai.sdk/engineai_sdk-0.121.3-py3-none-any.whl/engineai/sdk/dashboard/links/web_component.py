"""Internal SDK WebComponent Link."""

from typing import List

from engineai.sdk.dashboard.base import AbstractLink
from engineai.sdk.dashboard.dependencies.web_component import WebComponentDependency
from engineai.sdk.dashboard.links.exceptions import WebComponentLinkMinimumPathError


class WebComponentLink(AbstractLink):
    """WebComponentLink is a link to a web component."""

    def __init__(self, path: List[str]) -> None:
        """Constructor for WebComponentLink Class.

        Args:
            path: path to the web component data. Represents the path to the data
                injected, e.g. ['path', 'to', 'data'], where 'data' is the field
                to be used.
        """
        if len(path) < 2:
            raise WebComponentLinkMinimumPathError
        self.__dependency = WebComponentDependency(path=path)

    @property
    def dependency(self) -> WebComponentDependency:
        """Returns dependency."""
        return self.__dependency

    def _generate_templated_string(self, *, selection: int = 0) -> str:  # noqa
        """Generates template string to be used in dependency."""
        return str(self.__dependency)
