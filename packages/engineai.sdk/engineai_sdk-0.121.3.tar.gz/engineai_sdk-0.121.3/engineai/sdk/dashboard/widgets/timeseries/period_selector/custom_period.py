"""Spec for a custom period for a period selector."""

from datetime import datetime
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links.abstract import AbstractFactoryLinkItemsHandler
from engineai.sdk.dashboard.widgets.timeseries.exceptions import (
    TimeseriesPeriodSelectorDatesDefinitionError,
)


class CustomPeriod(AbstractFactoryLinkItemsHandler):
    """Define custom time intervals for period selector in Timeseries.

    Construct specifications for a custom period for a period selector
    component to define time intervals.
    """

    @type_check
    def __init__(
        self,
        *,
        label: Optional[str] = None,
        start_date: Union[str, datetime],
        end_date: Union[str, datetime],
    ) -> None:
        """Constructor for CustomPeriod.

        Args:
            label: label to show in period selector.
            start_date: start date of custom period in a format supported by
                pandas.to_datetime.
            end_date: end date of custom period in a format supported by
                pandas.to_datetime.

        Raises:
            TimeseriesPeriodSelectorDatesDefinitionError: if end_date <= start_date
        """
        super().__init__()
        self.__label = label
        self.__start_date = self.__get_datetime_in_milliseconds(start_date)
        self.__end_date = self.__get_datetime_in_milliseconds(end_date)
        if self.__end_date <= self.__start_date:
            raise TimeseriesPeriodSelectorDatesDefinitionError(
                self.__start_date, self.__end_date
            )

    def __get_datetime_in_milliseconds(self, date_time: Union[str, datetime]) -> int:
        if isinstance(date_time, str):
            aux_date = pd.to_datetime(date_time)
        else:
            aux_date = date_time
        return int(aux_date.timestamp() * 1000)

    def prepare(self, label: str) -> None:
        """Prepare custom period."""
        if self.__label is None:
            self.__label = label

    @property
    def label(self) -> str:
        """Returns label associated with custom period.

        Returns:
            str: label
        """
        return self.__label if self.__label else ""

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "label": self.__label,
            "startDate": self.__start_date,
            "endDate": self.__end_date,
        }
