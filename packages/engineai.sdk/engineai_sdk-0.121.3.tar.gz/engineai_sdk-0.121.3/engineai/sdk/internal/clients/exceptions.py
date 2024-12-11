"""Client Module Exceptions."""

from typing import Optional

from engineai.sdk.dashboard.exceptions import EngineAIDashboardError


class DashboardClientError(EngineAIDashboardError):
    """Base Client Module Error class for all Client Errors."""


class APIServerError(DashboardClientError):
    """Exception raised when there is an error from the API."""

    def __init__(
        self,
        request_id: str,
        error: str,
        error_code: Optional[str] = None,
        *args: object,
    ) -> None:
        """Construct for APIServerError class.

        Args:
            request_id (str): Request id
            error (str): error message.
            error_code (Optional[str]): error code.
        """
        super().__init__(request_id, error, error_code, *args)
        self.error_strings.append(f"Server error with request id {request_id}: {error}")


class APIUrlNotFoundError(DashboardClientError):
    """Exception raised when DASHBOARD_API_URL not set."""

    def __init__(self, *args: object) -> None:
        """Construct for APIUrlNotFound class."""
        super().__init__(*args)
        self.error_strings.append("Environment variable DASHBOARD_API_URL not set.")


class DashboardAPINoVersionFoundError(DashboardClientError):
    """Exception raised when cannot find the API version from the response content."""

    def __init__(self, *args: object) -> None:
        """Construct for DashboardAPINoVersionFoundError class."""
        super().__init__(*args)
        self.error_strings.append(
            "No version found when trying to fetch the DashboardAPI."
        )
