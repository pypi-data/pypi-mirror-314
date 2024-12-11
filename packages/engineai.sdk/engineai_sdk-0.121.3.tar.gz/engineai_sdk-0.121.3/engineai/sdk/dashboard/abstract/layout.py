"""Abstract Class implemented by main Dashboard Items."""

from abc import abstractmethod
from typing import List
from typing import Optional
from typing import Union

from typing_extensions import Unpack

from engineai.sdk.dashboard.abstract.typing import PrepareParams
from engineai.sdk.dashboard.base import AbstractFactory


class AbstractLayoutItem(AbstractFactory):
    """Abstract Class implemented by main Dashboard Items."""

    _INPUT_KEY: Optional[str] = None

    def __init__(self) -> None:
        """Creates a generic Vertical GridItem."""
        super().__init__()
        self.__dashboard_slug = ""

    @abstractmethod
    def items(self) -> List["AbstractLayoutItem"]:
        """Returns a list of items contained by the current item.

        Returns:
            List["AbstractLayoutItem"]: List of items contained by the current item.
        """

    @property
    @abstractmethod
    def height(self) -> float:
        """Returns height."""

    @property
    @abstractmethod
    def has_custom_heights(self) -> bool:
        """Returns if has custom heights."""

    @abstractmethod
    def prepare_heights(self, row_height: Optional[Union[int, float]] = None) -> None:
        """Prepare heights."""

    @abstractmethod
    def prepare(self, **kwargs: Unpack[PrepareParams]) -> None:
        """Prepare tab.

        Args:
            **kwargs (Unpack[PrepareParams]): keyword arguments
        """

    @property
    def dashboard_slug(self) -> str:
        """Returns items dashboard slug.

        Returns:
            str: dashboard slug
        """
        return self.__dashboard_slug

    @dashboard_slug.setter
    def dashboard_slug(self, dashboard_slug: str) -> None:
        """Sets the item's dashboard slug."""
        self.__dashboard_slug = dashboard_slug

    @property
    def input_key(self) -> str:
        """Return input type argument value.

        All Select Layout Items must now have the _INPUT_KEY defined.
        """
        if self._INPUT_KEY is None:
            msg = f"Class {self.__class__.__name__}._INPUT_KEY not defined."
            raise NotImplementedError(msg)
        return self._INPUT_KEY
