"""Spec for MarkdownItem class."""

from typing import Any
from typing import Dict

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.widgets.content.exceptions import ContentItemNoValueError


class MarkdownItem(AbstractFactory):
    """Spec for MarkdownItem class."""

    @type_check
    def __init__(self, data_key: str) -> None:
        """Construct spec for MarkdownItem class.

        Args:
            data_key (str): Key inside the data with the content
                for the markdown Item
        """
        super().__init__()
        self.__data_key = data_key

    def validate(
        self,
        *,
        data: Dict[str, Any],
    ) -> None:
        """Validates MarkdownItem specs.

        Args:
            data (Dict[str, Any]): data associated to the path.
        """
        if self.__data_key not in data:
            raise ContentItemNoValueError(
                data_key="data_key",
                data_key_value=self.__data_key,
                class_name=self.__class__.__name__,
            )

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {"dataKey": self.__data_key}
