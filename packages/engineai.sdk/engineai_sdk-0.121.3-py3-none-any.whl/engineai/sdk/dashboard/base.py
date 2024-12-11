"""Top-level package for Dashboard factories."""

import logging
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import Optional

logger = logging.getLogger(__name__)

HEIGHT_ROUND_VALUE = 2


class AbstractFactory(ABC):
    """Abstract Class implemented by all factories."""

    @abstractmethod
    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """


class DependencyInterface(AbstractFactory):
    """Generic interface for dependencies."""

    _INPUT_KEY: Optional[str] = None

    @property
    def input_key(self) -> str:
        """Input Key."""
        if self._INPUT_KEY is None:
            msg = f"Class {self.__class__.__name__}._INPUT_KEY not defined."
            raise NotImplementedError(msg)
        return self._INPUT_KEY

    def prepare(self, _: str) -> None:
        """Prepare dependency."""
        return


class AbstractLink:
    """Abstract class to implement links."""

    def __str__(self) -> str:
        return self._generate_templated_string()

    @property
    def link_component(self) -> Any:
        """Return link component.

        Widget for WidgetField
        Route for RouteLink
        """

    @property
    @abstractmethod
    def dependency(self) -> DependencyInterface:
        """Return DependencyInterface."""

    @abstractmethod
    def _generate_templated_string(self, *, selection: int = 0) -> str:
        """Generates template string to be used in dependency."""
