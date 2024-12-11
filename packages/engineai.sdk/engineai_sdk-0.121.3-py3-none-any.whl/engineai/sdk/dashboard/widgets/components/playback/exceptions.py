"""Playback Exceptions."""

from engineai.sdk.dashboard.exceptions import BaseDataValidationError
from engineai.sdk.dashboard.widgets.exceptions import DashboardWidgetError


class PlaybackError(DashboardWidgetError):
    """Playback Base Exception."""

    CLASS_NAME = "Playback"


class PlaybackItemsValidateNoDataColumnError(BaseDataValidationError):
    """Playback Widgets Validate No DataColumn Error."""

    def __init__(
        self,
        missing_column_name: str,
        missing_column: str,
    ) -> None:
        """Constructor for PlaybackItemsValidateNoDataColumnError class.

        Args:
            missing_column_name: Missing column name
            missing_column: Missing column value
        """
        message = f"'{missing_column_name}={missing_column}' not found in Data."
        super().__init__(message)


class PlaybackNegativeUpdateIntervalError(PlaybackError):
    """Playback Negative Update Interval Error."""

    def __init__(self, *args: object) -> None:
        """Constructor for PlaybackNegativeUpdateIntervalError class."""
        super().__init__(None, *args)
        self.error_strings.append("'update_interval' should be higher that 0.")
