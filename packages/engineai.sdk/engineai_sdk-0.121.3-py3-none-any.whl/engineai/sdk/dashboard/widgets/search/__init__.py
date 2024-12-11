"""Specs for Search Widgets components."""

from .results.number import ResultNumberItem
from .results.styling.number import ResultNumberStyling
from .results.styling.text import ResultTextStyling
from .results.text import ResultTextItem
from .search import Search

__all__ = [
    "Search",
    "ResultTextItem",
    "ResultNumberItem",
    "ResultTextStyling",
    "ResultNumberStyling",
]
