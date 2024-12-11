"""Map Exceptions."""

from typing import Any

from engineai.sdk.dashboard.exceptions import BaseDataValidationError
from engineai.sdk.dashboard.widgets.exceptions import DashboardWidgetError


class MapError(DashboardWidgetError):
    """Map Base Exception."""


class MapDuplicateSeriesError(MapError):
    """Duplicate Map Series Error."""

    def __init__(
        self, widget_id: str, class_name: str, series_name: str, *args: object
    ) -> None:
        """Construct for MapDuplicateSeriesError class."""
        self.CLASS_NAME = class_name
        super().__init__(None, widget_id, series_name, *args)
        self.error_strings.append(f"A series with name `{series_name}` already exists")


class MapColumnDataNotFoundError(BaseDataValidationError):
    """Column containing data not found Error."""

    def __init__(self, column_data: Any) -> None:
        """Constructor for MapColumnDataNotFoundError class."""
        super().__init__(f"Missing {column_data=} in Data.")
