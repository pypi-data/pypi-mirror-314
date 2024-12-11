"""Dashboard Module Exceptions."""

from typing import List
from typing import Optional

from engineai.sdk.dashboard.exceptions import DashboardError
from engineai.sdk.dashboard.exceptions import EngineAIDashboardError


class DashboardInvalidSlugError(DashboardError):
    """Dashboard invalid slug error."""

    def __init__(self, slug: str, *args: object) -> None:
        """Constructor for DashboardInvalidSlugError class.

        Args:
            slug (str): widget type.
        """
        super().__init__(slug, *args)
        self.error_strings.append(
            "Slug value can only contain lower case alphanumeric and underscore "
            "character and must end with a alphanumeric character."
        )


class DashboardVersionValueError(DashboardError):
    """Dashboard Version Value Error Exception."""

    def __init__(self, slug: str, *args: object) -> None:
        """Constructor for DashboardVersionValueError class."""
        super().__init__(slug, *args)
        self.error_strings.append(
            "Dashboard `version` does not comply the semantic versioning. "
            "Use <major>.<minor>.<patch> system, e.g. 1.2.0."
        )


class DashboardDuplicatedWidgetIdsError(DashboardError):
    """Dashboard Duplicated Widgets Ids Exception."""

    def __init__(self, slug: str, widget_ids: List[str], *args: object) -> None:
        """Constructor for DashboardDuplicatedWidgetIdsError class.

        Args:
            slug (str): widget type.
            widget_ids (List[str]): List of widgets not in the dashboard.
        """
        super().__init__(slug, widget_ids, *args)
        self.error_strings.append(f"Widgets with id {widget_ids} duplicated.")


class MetadataLastAvailableDataTypeError(EngineAIDashboardError):
    """Metadata Last Available Data Type Error Exception."""

    def __init__(self) -> None:
        """Constructor for MetadataLastAvailableDataTypeError class."""
        super().__init__()
        self.error_strings.append(
            "Can only set datetime or None type values in 'last_available_date'."
        )


class DashboardWidgetLinkDefinedAfterError(EngineAIDashboardError):
    """Dashboard Widget Link Defined After Exception."""

    def __init__(
        self, widget_field_widget_id: str, widget_id: str, *args: object
    ) -> None:
        """Constructor for DashboardWidgetLinkDefinedAfterError class.

        Args:
            widget_field_widget_id (str): WidgetField's widget id.
            widget_id (str): current widget id.
        """
        super().__init__(widget_id, widget_field_widget_id, *args)
        self.error_strings.append(
            f"SelectableWidget with widget_id={widget_field_widget_id} has to "
            f"be defined before the Widget with {widget_id=} that uses it as "
            "dependency."
        )


class DashboardNoDashboardFoundError(EngineAIDashboardError):
    """Exception raised when cannot find the API dashboard from the response content."""

    def __init__(
        self,
        slug: str,
        app_slug: Optional[str],
        workspace_slug: Optional[str],
        version: Optional[str],
        *args: object,
    ) -> None:
        """Construct for DashboardAPINoDashboardFoundError class."""
        super().__init__(slug, app_slug, version, *args)
        version = f" and {version=}" if version else ""
        self.error_strings.append(
            f"No Dashboard found with {slug=}{version} in your app with "
            f"{workspace_slug=} and {app_slug=}. Please create the Dashboard "
            "first, before using skip_data flag."
        )


class DashboardSkipDataCannotCreateRunError(EngineAIDashboardError):
    """Exception raised when cannot create run and skip data at the same time."""

    def __init__(self, *args: object) -> None:
        """Construct for DashboardSkipDataCannotCreateRunError class."""
        super().__init__(*args)
        self.error_strings.append(
            "To use skip_data flag, you should set the publish mode to DEFAULT."
        )


class DashboardDuplicatedPathsError(EngineAIDashboardError):
    """Exception raised when dashboard pages have the same path."""

    def __init__(self, duplicated_path: str, *args: object) -> None:
        """Construct for DashboardDuplicatedPathsError class."""
        super().__init__(duplicated_path, *args)
        self.error_strings.append(f"Dashboard has pages with {duplicated_path=}")


class DashboardEmptyContentError(EngineAIDashboardError):
    """Exception raised when dashboard content is empty."""

    def __init__(self, *args: object) -> None:
        """Construct for DashboardEmptyContentError class."""
        super().__init__(*args)
        self.error_strings.append(
            "No content found. Please add content to the dashboard."
        )
