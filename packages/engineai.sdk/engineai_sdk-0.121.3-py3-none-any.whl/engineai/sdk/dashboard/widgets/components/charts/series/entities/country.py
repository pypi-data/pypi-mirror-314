"""Chart Series Country Entity."""

from typing import Any
from typing import Dict

import pandas as pd

from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.charts.exceptions import (
    ChartSeriesEntityInvalidCountryCodeError,
)
from engineai.sdk.dashboard.widgets.components.charts.exceptions import (
    ChartSeriesEntityNoDataColumnError,
)
from engineai.sdk.dashboard.widgets.components.charts.series.entities.base import Entity
from engineai.sdk.dashboard.widgets.utils import COUNTRY_CODES


class CountryEntity(Entity):
    """Country entity spec."""

    _INPUT_KEY = "country"

    def __init__(
        self, country_code: TemplatedStringItem, show_flag: bool = True
    ) -> None:
        """Construct country entity.

        Args:
            country_code: country code.
            show_flag: show country flag.
        """
        super().__init__()
        self.__country_code = country_code
        self.__flag = show_flag

    def validate_data_column(self, data: pd.DataFrame) -> None:
        """Validate entity data.

        Args:
            data: Dataframe to validate against.
        """
        if (
            isinstance(self.__country_code, str)
            and self.__country_code not in data.columns
        ):
            raise ChartSeriesEntityNoDataColumnError(
                self.__class__.__name__, self.__country_code
            )

    def validate_country_code(self) -> None:
        """Validate country code.

        Args:
            data: Dataframe to validate against.
        """
        if (
            isinstance(self.__country_code, str)
            and self.__country_code not in COUNTRY_CODES
        ):
            raise ChartSeriesEntityInvalidCountryCodeError(
                self.__class__.__name__, self.__country_code
            )

    def _build_entity(self) -> Dict[str, Any]:
        return {
            "countryCodeKey": build_templated_strings(items=self.__country_code),
            "showFlag": self.__flag,
        }
