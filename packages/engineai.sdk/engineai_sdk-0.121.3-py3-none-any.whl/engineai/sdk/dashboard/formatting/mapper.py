"""Formatting spec for Key/Value."""

from typing import Any
from typing import Dict
from typing import List
from typing import Mapping

from engineai.sdk.dashboard.formatting.base import BaseFormatting


class MapperFormatting(BaseFormatting):
    """Factory class to map a column with ordinal numbers to text.

    Factory class to map ordinal numbers to text
    labels for categorical data.
    """

    _INPUT_KEY = "mapper"

    def __init__(self, *, mapping: Mapping[int, str]) -> None:
        """Constructor for MapperFormatting.

        Args:
            mapping (Mapping[int, str]): mapping between number and text label.
        """
        super().__init__()
        self.__mapping = mapping

    @property
    def mapping(self) -> Mapping[int, str]:
        """Returns formatting mapping between integer numbers and labels.

        Returns:
            Mapping[int, str]: formatting mapping
        """
        return self.__mapping

    def _build_mapping(self) -> List[Dict[str, Any]]:
        return [
            {"key": str(key), "value": self.__mapping[key]} for key in self.__mapping
        ]

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {"mapping": self._build_mapping()}
