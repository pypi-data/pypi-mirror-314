"""Base classes for formatting."""

from typing import Any
from typing import Dict
from typing import Optional

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.links.abstract import AbstractFactoryLinkItemsHandler


class BaseFormatting(AbstractFactory):
    """Base class for formatting."""

    _INPUT_KEY: Optional[str] = None

    def __init__(self) -> None:
        """Constructor for BaseFormatting."""
        super().__init__()

    @property
    def input_key(self) -> str:
        """Returns input key."""
        if self._INPUT_KEY is None:
            msg = "Input key is not defined for this formatting class."
            raise NotImplementedError(msg)
        return self._INPUT_KEY

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {}

    def build_formatting(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {self.input_key: self.build()}


class BaseNumberFormatting(AbstractFactoryLinkItemsHandler):
    """Base class for formatting."""

    _INPUT_KEY: Optional[str] = None

    def __init__(self) -> None:
        """Constructor for BaseNumberFormatting."""
        super().__init__()

    @property
    def input_key(self) -> str:
        """Returns input key."""
        if self._INPUT_KEY is None:
            msg = "Input key is not defined for this formatting class."
            raise NotImplementedError(msg)
        return self._INPUT_KEY

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {}

    def build_formatting(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {self.input_key: self.build()}
