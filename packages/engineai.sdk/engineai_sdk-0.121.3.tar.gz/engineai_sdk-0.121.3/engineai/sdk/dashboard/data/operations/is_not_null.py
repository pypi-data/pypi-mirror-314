"""Specs for IsNotNull."""

from typing import Any
from typing import Dict

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings

from .base import BaseOperation


class IsNotNull(BaseOperation):
    """Specs for IsNotNull."""

    _ITEM_ID = "exists"

    @type_check
    def __init__(self, *, data_column: TemplatedStringItem) -> None:
        """Construct for IsNotNull class.

        Args:
            data_column: data filter column.
        """
        super().__init__()
        self.__data_column = data_column

    def build_filter(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "dataKey": build_templated_strings(items=self.__data_column),
        }
