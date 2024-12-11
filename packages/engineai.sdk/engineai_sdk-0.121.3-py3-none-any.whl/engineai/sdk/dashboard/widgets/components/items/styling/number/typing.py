"""Typings for Number Item Stylings."""

from typing import Union

from .chip import NumberStylingChip
from .dot import NumberStylingDot
from .font import NumberStylingFont
from .progress_bar import NumberStylingProgressBar

NumberItemStyling = Union[
    NumberStylingFont, NumberStylingDot, NumberStylingChip, NumberStylingProgressBar
]
