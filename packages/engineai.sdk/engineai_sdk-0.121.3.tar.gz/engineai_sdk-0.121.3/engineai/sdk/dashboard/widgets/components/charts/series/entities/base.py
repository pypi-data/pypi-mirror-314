"""Chart Series Entities base."""

from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import Optional

from engineai.sdk.dashboard.links.abstract import AbstractFactoryLinkItemsHandler


class Entity(AbstractFactoryLinkItemsHandler):
    """Chart Series Entities base spec."""

    _INPUT_KEY: Optional[str] = None

    @property
    def _input_key(self) -> str:
        """Returns Input Key argument value."""
        if self._INPUT_KEY is None:
            msg = f"Class {self.__class__.__name__}._INPUT_KEY not defined."
            raise NotImplementedError(msg)
        return self._INPUT_KEY

    @abstractmethod
    def _build_entity(self) -> Dict[str, Any]:
        pass

    def build(self) -> Dict[str, Any]:
        """Build entities Input spec."""
        return {
            self._input_key: self._build_entity(),
        }
