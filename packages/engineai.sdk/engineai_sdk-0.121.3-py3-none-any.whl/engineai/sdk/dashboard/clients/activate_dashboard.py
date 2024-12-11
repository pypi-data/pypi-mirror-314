"""Spec for a activate dashboard."""

from typing import Any
from typing import Dict
from typing import Optional


class ActivateDashboardVersion:
    """Spec for ActivateDashboardVersion class."""

    def __init__(self, version: str, activate: bool) -> None:
        """Construct for ActivateDashboardVersion class.

        Args:
            version: Dashboard version.
            activate: flag to indicate version is to become active or not.
        """
        self.__version = version
        self.__activate = activate

    @property
    def version(self) -> str:
        """Version."""
        return self.__version

    @property
    def activate(self) -> bool:
        """Activate."""
        return self.__activate

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API."""
        return {
            "version": self.__version,
            "activate": self.__activate,
        }


class ActivateDashboardRun:
    """Spec for ActivateDashboardRun class."""

    def __init__(self, run: str, activate: bool) -> None:
        """Construct for ActivateDashboardRun class.

        Args:
            run: Dashboard run.
            activate: flag to indicate run is to become active or not.
        """
        self.__run = run
        self.__activate = activate

    @property
    def run(self) -> str:
        """Run."""
        return self.__run

    @property
    def activate(self) -> bool:
        """Activate."""
        return self.__activate

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API."""
        return {
            "run": self.__run,
            "activate": self.__activate,
        }


class ActivateDashboard:
    """Spec for ActivateDashboard class."""

    def __init__(
        self,
        *,
        dashboard_id: str,
        version: Optional[str],
        activate_version: bool = True,
        run: Optional[str],
        activate_run: bool = True,
    ) -> None:
        """Construct for ActivateDashboard class.

        Args:
            dashboard_id: Dashboard id.
            version: Dashboard version.
            activate_version: flag to indicate version is to become active or not.
            run: Dashboard run.
            activate_run: flag to indicate run is to become active or not.
        """
        self.__dashboard_id = dashboard_id
        self.__version = ActivateDashboardVersion(
            version=version if version is not None else "none",
            activate=activate_version,
        )
        self.__run = ActivateDashboardRun(
            run=run if run is not None else "none", activate=activate_run
        )

    @property
    def dashboard_id(self) -> str:
        """Dashboard Id."""
        return self.__dashboard_id

    @property
    def version(self) -> str:
        """Version."""
        return self.__version.version

    @property
    def activate_version(self) -> bool:
        """Activate version."""
        return self.__version.activate

    @property
    def run(self) -> str:
        """Run."""
        return self.__run.run

    @property
    def activate_run(self) -> bool:
        """Activate run."""
        return self.__run.activate

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API."""
        return {
            "id": self.__dashboard_id,
            "version": self.__version.build(),
            "run": self.__run.build(),
        }
