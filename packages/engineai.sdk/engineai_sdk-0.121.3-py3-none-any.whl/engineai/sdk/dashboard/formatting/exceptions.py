"""Formatting exceptions."""

from typing import Optional

from engineai.sdk.dashboard.exceptions import EngineAIDashboardError


class DashboardFormattingError(EngineAIDashboardError):
    """Dashboard Formatting Exception."""

    CLASS_NAME: Optional[str] = None

    def __init__(self, *args: object) -> None:
        """Constructor for Dashboard Widget Exception."""
        super().__init__(*args)
        self.error_strings.append(f"{self._class_name} error.")

    @property
    def _class_name(self) -> str:
        if self.CLASS_NAME is None:
            msg = "Variable CLASS_NAME not implemented."
            raise NotImplementedError(msg)
        return self.CLASS_NAME
