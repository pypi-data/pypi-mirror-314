"""Formatting spec for text."""

from typing import Any
from typing import Dict
from typing import Optional

from engineai.sdk.dashboard.formatting.base import BaseFormatting


class TextFormatting(BaseFormatting):
    """Customize maximum characters and splitting options.

    Description for formatting text, allowing customization
    of maximum characters and splitting.
    """

    _INPUT_KEY = "text"

    def __init__(
        self, *, max_characters: int = 30, split: Optional[str] = None
    ) -> None:
        """Constructor for TextFormatting.

        Args:
            max_characters (int): number of characters to show before text is trimmed.
                If len(text) > max_characters, text is trimmed to max_characters and
                ... are added and full text shown on hover.
                Defaults to 30.
            split (Optional[str]): split character to determine first word.
                After split character, ... are added and full text shown on hover.
                Defaults to None.
        """
        super().__init__()
        self.__max_characters = max_characters
        self.__split = split

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "maxCharacters": self.__max_characters,
            "split": self.__split,
        }
