"""Spec for period selector of a timeseries widget."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.widgets.timeseries.exceptions import (
    TimeseriesPeriodSelectorHiddenPeriodsError,
)
from engineai.sdk.dashboard.widgets.timeseries.exceptions import (
    TimeseriesPeriodSelectorNoAvailableDefaultOptionError,
)

from .custom_period import CustomPeriod
from .period import PeriodType
from .period import build_timeseries_period
from .standard import Period


class PeriodSelector(AbstractFactory):
    """Select predefined periods for Timeseries visualization.

    Construct specifications for a period selector component of a
    timeseries widget, select predefined periods for data visualization.
    """

    @type_check
    def __init__(
        self,
        *periods: PeriodType,
        default_selection: Optional[int] = None,
        visible: bool = True,
    ) -> None:
        """Constructor for PeriodSelector.

        Args:
            periods: specs for periods added into timeseries widget
                period selector component.
            default_selection: choose which period selector to be the default.
            visible: flag that makes the period selector visible.
                If False, all periods added and default selection will be ignored.

        Raises:
            TimeseriesPeriodSelectorEmptyDefinitionError: when `periods` is empty.
            TimeseriesPeriodSelectorNoAvailableDefaultOptionError: when the
                desired default selection element does not exist
        """
        super().__init__()
        self.__validate(*periods, visible=visible)
        self.__selected: str
        self.__option = default_selection
        self.__visible = visible

        self.__set_periods(*periods)
        self.__set_default_selection(self.__option)

    def __validate(self, *periods: PeriodType, visible: bool) -> None:
        if len(periods) > 0 and not visible:
            raise TimeseriesPeriodSelectorHiddenPeriodsError

    def __set_periods(self, *periods: PeriodType) -> None:
        if self.__visible:
            default: List[PeriodType] = [  # Short Term Periods
                Period.M1,
                Period.YTD,
                Period.Y1,
                Period.Y5,
                Period.ALL,
            ]

            self.__periods: List[PeriodType] = (
                default if len(periods) == 0 else list(periods)
            )
            if self.__option is None:
                self.__set_default_selection(3 if self.__periods == default else 1)
        else:
            self.__periods = []
            self.__selected = ""

    def __set_default_selection(self, option: Optional[int] = None) -> None:
        if self.__visible and option is not None:
            if len(self.__periods) < option or option <= 0:
                raise TimeseriesPeriodSelectorNoAvailableDefaultOptionError(
                    len(self.__periods), option
                )
            self.__selected = self.__periods[option - 1].label

    def prepare(self) -> None:
        """Validate Period Selector specs.

        Raises:
            TimeseriesPeriodSelectorDuplicatedLabelsError: when two periods have the
                same label
            TimeseriesPeriodSelectorUnorderedPeriodsError: when added periods are not
                ordered in a timeline way
        """
        self._custom_periods_prepare()

    def _custom_periods_prepare(self) -> None:
        custom_periods = [
            period for period in self.__periods if isinstance(period, CustomPeriod)
        ]

        if len(custom_periods) == 1:
            custom_periods[0].prepare("Custom Period")
        else:
            for i in range(len(custom_periods)):
                custom_periods[i].prepare("Period " + str(i + 1))

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "periods": (
                [build_timeseries_period(period=period) for period in self.__periods]
                if self.__periods
                else []
            ),
            "selected": self.__selected,
            "isDatePickerVisible": self.__visible,
        }
