"""Typing for text tile matrix items."""

from typing import Union

from engineai.sdk.dashboard.widgets.components.items.styling import TextStylingDot
from engineai.sdk.dashboard.widgets.components.items.styling import TextStylingFont

from .styling.background import TextStylingBackground

TileMatrixTextItemStyling = Union[
    TextStylingDot,
    TextStylingFont,
    TextStylingBackground,
]
