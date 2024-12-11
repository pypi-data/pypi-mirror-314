"""Spec for Tile Matrix Styling Background."""

from typing import Optional

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.styling.color.typing import ColorSpec
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.widgets.components.items.styling.base import BaseItemStyling


class NumberStylingBackground(BaseItemStyling):
    """Spec for Tile Matrix Styling Background class."""

    _INPUT_KEY: str = "background"

    @type_check
    def __init__(
        self,
        *,
        color_spec: Optional[ColorSpec] = None,
        data_column: Optional[TemplatedStringItem] = None,
    ) -> None:
        """Construct spec for TileMatrixStylingBackground class.

        Args:
            color_spec: specs for color.
            data_column: styling value key.
        """
        super().__init__(data_column=data_column, color_spec=color_spec)
