"""Typings for Text Item Stylings."""

from typing import Union

from .chip import TextStylingChip
from .country_flag import TextStylingCountryFlag
from .dot import TextStylingDot
from .font import TextStylingFont

TextItemStyling = Union[
    TextStylingChip,
    TextStylingCountryFlag,
    TextStylingDot,
    TextStylingFont,
]
