"""Typings for layout modules."""

from typing import Union

from engineai.sdk.dashboard.interface import CardInterface as Card
from engineai.sdk.dashboard.interface import GridInterface as Grid
from engineai.sdk.dashboard.interface import SelectableInterface as SelectableSection
from engineai.sdk.dashboard.interface import WidgetInterface as Widget

LayoutItem = Union[Widget, Card, Grid, SelectableSection]
"""
Base class for items in dashboard layout; inherited by other layout-related classes.

The LayoutItem class is a module attribute, representing the base class for items
in a dashboard layout. It's a common type that other layout-related classes
inherit from.
"""
