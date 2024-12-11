"""Dashboard base Exception."""

from typing import List


class EngineAIDashboardError(Exception):
    """Base Exception class for all Dashboard Errors.

    Raises:
        EngineAIDashboardError: Platform SDK Dashboard base error.
    """

    def __init__(self, *args: object) -> None:
        """Base Exception class for all Dashboard Errors."""
        super().__init__(*args)
        self.error_strings = ["Platform SDK Dashboard Error occurred:"]

    def __str__(self) -> str:
        return " ".join(self.error_strings)


class EngineAIDashboardWarning(UserWarning):
    """Base Warning class for all Dashboard Warnings.

    Raises:
        EngineAIDashboardWarning: Dashboard base warning.
    """

    def __init__(self, *args: object) -> None:
        """Base Warning class for all Dashboard Warnings."""
        super().__init__(*args)
        self.error_strings = ["Dashboard Factory Warning:"]

    def __str__(self) -> str:
        return " ".join(self.error_strings)


class ImproperlyConfiguredError(Exception):
    """Dashboard Improperly Configured Exception."""


class WidgetDataNotFoundError(EngineAIDashboardError):
    """Dashboard Widget Data Not Found Exception."""

    def __init__(self, widget_id: str, *args: object) -> None:
        """Dashboard Widget Data Not Found Exception.

        Args:
            widget_id (str): Unique widget ID in the dashboard.
        """
        super().__init__(
            widget_id,
            *args,
        )
        self.error_strings.append(
            f"No data found for widget {widget_id=}.",
        )


class WidgetFieldNotFoundError(EngineAIDashboardError):
    """Dashboard Widget Field Not Found Exception."""

    def __init__(self, field: str, columns: List[str], *args: object) -> None:
        """Dashboard Widget Field Not Found Exception.

        Args:
            field (str): id of field exposed by widget.
            columns (List[str]): dataframe data columns.
        """
        super().__init__(
            field,
            columns,
            *args,
        )
        self.error_strings.append(
            f"{field=} is not available in data found. "
            f"Available columns: {columns=}.",
        )


class DataFieldNotFoundError(EngineAIDashboardError):
    """Dashboard Data Field Not Found Exception."""

    def __init__(self, field: str, *args: object) -> None:
        """Dashboard Data Field Not Found Exception.

        Args:
            field (str): id of field exposed by DataField.
        """
        super().__init__(
            field,
            *args,
        )
        self.error_strings.append(
            f"{field=} was not found in the data and a default value was not provided."
        )


class DataFieldInItemIDKeyNotFoundError(EngineAIDashboardError):
    """Dashboard Factory Data Field Not Found Exception."""

    def __init__(self, field: str, item_id_key: str, *args: object) -> None:
        """Dashboard Factory Data Field Not Found Exception.

        Args:
            field (str): id of field exposed by DataField.
            item_id_key: (str): key in data used to identify the data that feeds item.
        """
        super().__init__(
            field,
            item_id_key,
            *args,
        )
        self.error_strings.append(
            f"{field=} was not found in item with {item_id_key} and a default value "
            "was not provided."
        )


class DataFieldColumnNameNotProvidedError(EngineAIDashboardError):
    """Dashboard Data Field Not Found Exception."""

    def __init__(self, *args: object) -> None:
        """Dashboard Data Field Not Found Exception.

        Args:
            field (str): id of field exposed by DataField.
        """
        super().__init__(
            *args,
        )
        self.error_strings.append(
            "Please provide a column name and a node when using warning flags"
        )


class ToggleFeatureMissingVersionError(EngineAIDashboardError):
    """Toggle Version Missing Wrong Error."""

    def __init__(self, *args: object) -> None:
        """Toggle Version Wrong Format Error."""
        super().__init__(
            *args,
        )
        self.error_strings.append(
            "Initializing ToggleVersion without a value for version argument.",
        )


class ToggleFeatureWrongFormatError(EngineAIDashboardError):
    """Toggle Version Wrong Format Error.

    Args:
        version(str): version value.
    """

    def __init__(self, version: str, *args: object) -> None:
        """Toggle Version Wrong Format Error."""
        super().__init__(
            version,
            *args,
        )
        self.error_strings.append(
            f"Wrong version format for {version=}.",
        )


class DashboardError(EngineAIDashboardError):
    """Dashboard base Exception."""

    def __init__(self, slug: str, *args: object) -> None:
        """Constructor for DashboardError class.

        Args:
            slug (str): widget type.
        """
        super().__init__(slug, *args)
        self.error_strings.append(f"Dashboard with {slug=}.")


class BaseDataValidationError(Exception):
    """Base Exception class for all Data Validation Errors."""
