"""Formatting typing."""

from typing import Union

from .datetime import DateTimeFormatting
from .mapper import MapperFormatting
from .number import NumberFormatting
from .text import TextFormatting

FormattingType = Union[
    DateTimeFormatting, MapperFormatting, NumberFormatting, TextFormatting
]

__all__ = ["FormattingType"]
