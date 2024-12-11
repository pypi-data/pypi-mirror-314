"""Typings for Number Item Styling."""

from typing import Union

from engineai.sdk.dashboard.widgets.components.items.styling import NumberStylingArrow
from engineai.sdk.dashboard.widgets.components.items.styling import NumberStylingChip
from engineai.sdk.dashboard.widgets.components.items.styling import NumberStylingDot
from engineai.sdk.dashboard.widgets.components.items.styling import NumberStylingFont

from .styling.background import NumberStylingBackground
from .styling.background_arrow import NumberStylingBackgroundArrow

TileMatrixNumberItemStyling = Union[
    NumberStylingArrow,
    NumberStylingChip,
    NumberStylingDot,
    NumberStylingFont,
    NumberStylingBackground,
    NumberStylingBackgroundArrow,
]
