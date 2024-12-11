"""Dashboard version class."""

import re
import warnings
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union
from typing import cast

from typing_extensions import Unpack

from engineai.sdk.dashboard import config
from engineai.sdk.dashboard.abstract.typing import PrepareParams
from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.dashboard.enums import DashboardStatus
from engineai.sdk.dashboard.dashboard.exceptions import DashboardVersionValueError
from engineai.sdk.dashboard.dashboard.exceptions import (
    MetadataLastAvailableDataTypeError,
)


class DashboardVersion(AbstractFactory):
    """Spec for Dashboard version."""

    def __init__(
        self,
        slug: str,
        version: Optional[str],
        last_available_data: Optional[Union[datetime, List[str]]] = None,
        status: Optional[DashboardStatus] = None,
        create_run: bool = False,
    ) -> None:
        """Construct DashboardVersion Class.

        Args:
            slug: dashboard slug.
            version: version of the dashboard. Should be a valid
                semantic version (e.g. 1.0.0).
            last_available_data: value to store the last data that was used in
                the dashboard. The value can come directly from the argument or
                found in a face path.
            status: optional field that is used to tag
                the dashboard status.
            create_run: create run for dashboard. If true the API will create a run,
                if false the API will pick the active run, if there isn't one it will
                be created as none.
        """
        self.__slug = slug
        self.__version = self.__set_version(version) if version is not None else "none"
        self.__last_available_data = last_available_data
        self.__status = status
        self.__create_run = create_run

    @property
    def version(self) -> str:
        """Returns the version of the dashboard."""
        return self.__version

    def __set_version(self, version: str) -> str:
        """Get the version for the dashboard."""
        result = (
            config.DASHBOARD_VERSION
            if config.DASHBOARD_VERSION is not None
            else version
        )

        if not re.match(r"(\d+)\.(\d+)\.(\d+)", result):
            raise DashboardVersionValueError(slug=self.__slug)

        return result

    @property
    def last_available_data(self) -> Optional[Union[datetime, List[str]]]:
        """Returns Last Available Data.

        Returns:
            Optional[Union[datetime, List[str]]]: last available data
        """
        return self.__last_available_data

    @last_available_data.setter
    def last_available_data(self, last_available_data: Optional[datetime]) -> None:
        if last_available_data is not None and not isinstance(
            last_available_data, datetime
        ):
            raise MetadataLastAvailableDataTypeError
        self.__last_available_data = last_available_data

    @property
    def _get_last_available_data(self) -> Optional[Union[int, float]]:
        if self.__last_available_data is not None and not isinstance(
            self.__last_available_data, datetime
        ):
            raise MetadataLastAvailableDataTypeError

        if self.__last_available_data is not None:
            timestamp = self.__last_available_data.timestamp()
            if len(str(int(timestamp))) == 10:
                timestamp = timestamp * 1000
            return timestamp
        return None

    def prepare(self, **kwargs: Unpack[PrepareParams]) -> None:
        """Prepare the DashboardVersion object."""
        if (
            self.__version is not None
            and self.__last_available_data is not None
            and isinstance(self.__last_available_data, list)
        ):
            date = kwargs["storage"].get(
                "/".join(self.__last_available_data), default=None
            )

            if date is None:
                warnings.warn(
                    f"Cannot find `last_available_data` in path "
                    f"{self.__last_available_data}. "
                    f"Setting `last_available_data` to None."
                )

            self.__last_available_data = (
                datetime.fromtimestamp(cast(float, date)) if date is not None else date
            )

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API

        Raises:
            AttributeError: if widgets were added to dashboards but not to layout, or
                vice-versa.
        """
        return {
            "version": self.__version,
            "createRun": self.__create_run,
        }
