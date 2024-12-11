"""Country flag styling for tooltip items."""

from typing import Any
from typing import Dict

from engineai.sdk.dashboard.decorator import type_check

from .base import CountryTooltipItemStylingBase


class CountryTooltipItemStylingFlag(CountryTooltipItemStylingBase):
    """Country flag styling for tooltip items.

    Define specifications for a country item within a tooltip for a Chart
    widget to customize the appearance and content of tooltips displayed
    for country data.
    """

    _INPUT_KEY = "flag"

    @type_check
    def __init__(self, right_to_left: bool = False) -> None:
        """Construct country flag styling for tooltip items.

        Args:
            right_to_left: Enable right-to-left text direction.
        """
        self.__right_to_left = right_to_left

    def _build_styling(self) -> Dict[str, Any]:
        """Build country flag styling."""
        return {"rtl": self.__right_to_left}
