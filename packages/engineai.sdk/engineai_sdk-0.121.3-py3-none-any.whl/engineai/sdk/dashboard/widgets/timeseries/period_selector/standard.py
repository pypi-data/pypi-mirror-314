"""Spec for a standard period for a period selector."""

import enum


class Period(enum.Enum):
    """Standard time intervals for period selector in Timeseries.

    Defines standard periods for a period selector component to choose
    predefined time intervals for data visualization. Each period
    represents a lookback relative to the last date of the chart.

    Attributes:
        D1: 1 day.
        W1: 1 week.
        W2: 2 weeks.
        M1: 1 month.
        M3: 3 months.
        M6: 6 months.
        YTD: Year to date.
        Y1: 1 year.
        Y2: 2 years.
        Y3: 3 years.
        Y4: 4 years.
        Y5: 5 years.
        ALL: All data.

    """

    D1 = "D1"
    W1 = "W1"
    W2 = "W2"
    M1 = "M1"
    M3 = "M3"
    M6 = "M6"
    YTD = "YTD"
    Y1 = "Y1"
    Y2 = "Y2"
    Y3 = "Y3"
    Y4 = "Y4"
    Y5 = "Y5"
    ALL = "ALL"

    @property
    def index(self) -> int:
        """Returns index of element in enum.

        Small index are associated with short periods.

        Returns:
            int: index of element enum
        """
        values = list(Period.__members__.keys())
        return values.index(self.value)

    @property
    def label(self) -> str:
        """Returns label associated with standard period.

        Returns:
            str: label
        """
        return self.value
