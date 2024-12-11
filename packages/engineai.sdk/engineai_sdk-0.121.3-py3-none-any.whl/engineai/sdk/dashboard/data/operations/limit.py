"""Specs for Limit."""

from typing import Any
from typing import Dict
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings

from .base import BaseOperation


class Limit(BaseOperation):
    """Specs for Limit."""

    _ITEM_ID = "limit"

    @type_check
    def __init__(self, *, limit: Union[int, TemplatedStringItem]) -> None:
        """Construct for Limit class.

        Args:
            limit: query limit value.
        """
        super().__init__()
        self.__limit = str(limit) if isinstance(limit, int) else limit

    def build_filter(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "limit": build_templated_strings(items=self.__limit),
        }
