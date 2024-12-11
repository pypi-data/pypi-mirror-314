"""Web Component Dependencies Exceptions."""

from engineai.sdk.dashboard.exceptions import EngineAIDashboardError


class WebComponentMinimumPathError(EngineAIDashboardError):
    """Web Component Minimum Path Error."""

    def __init__(self) -> None:
        """Constructor for WebComponentMinimumPathError Class."""
        super().__init__()
        self.error_strings.append(
            "WebComponentMinimumPathError path have less then 2 paths. "
            "Example: ['path', 'to', 'data']"
        )
