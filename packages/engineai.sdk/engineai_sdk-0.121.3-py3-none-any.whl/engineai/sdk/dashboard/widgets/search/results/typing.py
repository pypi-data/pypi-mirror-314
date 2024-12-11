"""Search Widget Custom typing."""

from typing import Union

from engineai.sdk.dashboard.widgets.search.results.number import ResultNumberItem
from engineai.sdk.dashboard.widgets.search.results.text import ResultTextItem

ResultItemType = Union[ResultTextItem, ResultNumberItem]
