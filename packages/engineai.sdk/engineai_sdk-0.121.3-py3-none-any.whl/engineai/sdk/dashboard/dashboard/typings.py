"""Typings for dashboard modules."""

from typing import List
from typing import Union

from engineai.sdk.dashboard.interface import CollapsibleInterface as CollapsibleSection
from engineai.sdk.dashboard.layout.typings import LayoutItem

DashboardContent = Union[
    LayoutItem, List[Union[LayoutItem, CollapsibleSection]], CollapsibleSection
]
