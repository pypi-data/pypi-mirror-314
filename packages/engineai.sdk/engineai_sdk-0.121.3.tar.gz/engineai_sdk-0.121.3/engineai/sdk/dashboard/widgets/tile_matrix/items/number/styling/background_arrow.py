"""Spec for Tile Matrix Styling Background Arrow."""

from typing import Any
from typing import Dict
from typing import Optional

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.styling.color.divergent import Divergent
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.items.styling.base import BaseItemStyling


class NumberStylingBackgroundArrow(BaseItemStyling):
    """Spec for Tile Matrix Styling Background Arrow class."""

    _INPUT_KEY: str = "backgroundArrow"

    @type_check
    def __init__(
        self,
        *,
        color_divergent: Divergent,
        data_column: Optional[TemplatedStringItem] = None,
    ) -> None:
        """Construct spec for TileMatrixStylingBackgroundArrow class.

        Args:
            color_divergent: specs for color.
            data_column: styling value key.
        """
        super().__init__(
            data_column=data_column,
        )
        self.__color_divergent = color_divergent

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "divergentPalette": self.__color_divergent.build(),
            "valueKey": build_templated_strings(items=self.column),
        }
