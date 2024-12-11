"""Exceptions for Internal Links."""

from engineai.sdk.dashboard.exceptions import EngineAIDashboardError


class WebComponentLinkMinimumPathError(EngineAIDashboardError):
    """Web Component Link Minimum Path Error."""

    def __init__(self) -> None:
        """Constructor for WebComponentEmptyPathError Class."""
        super().__init__()
        self.error_strings.append(
            "WebComponentLink path have less then 2 paths. Please provide a path."
            "Example: ['path', 'to', 'data']"
        )
