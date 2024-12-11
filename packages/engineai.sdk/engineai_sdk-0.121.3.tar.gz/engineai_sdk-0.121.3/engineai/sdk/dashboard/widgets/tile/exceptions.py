"""Tile widget Exceptions."""

from engineai.sdk.dashboard.widgets.exceptions import DashboardWidgetError


class TileWidgetError(DashboardWidgetError):
    """Tile Widget Base Exception."""

    CLASS_NAME = "Tile"
