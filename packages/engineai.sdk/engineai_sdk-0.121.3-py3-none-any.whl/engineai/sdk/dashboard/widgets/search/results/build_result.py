"""Specs for build Search result."""

from typing import Any
from typing import Dict

from engineai.sdk.dashboard.widgets.search.results.number import ResultNumberItem
from engineai.sdk.dashboard.widgets.search.results.text import ResultTextItem

from .typing import ResultItemType


def build_search_result(item: ResultItemType) -> Dict[str, Any]:
    """Builds spec for dashboard API.

    Args:
        item: item spec

    Returns:
        Input object for Dashboard API
    """
    return {_get_input_key(item): item.build()}


def _get_input_key(item: ResultItemType) -> str:
    if isinstance(item, ResultNumberItem):
        return "number"
    if isinstance(item, ResultTextItem):
        return "text"
    msg = "item needs to be one of ResultTextItem, ResultNumberItem."
    raise TypeError(msg)
