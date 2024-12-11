"""Specs for dateitem item for a tooltip."""

from typing import Optional
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting import DateTimeFormatting
from engineai.sdk.dashboard.templated_string import DataField
from engineai.sdk.dashboard.templated_string import TemplatedStringItem

from .base import BaseTooltipItem


class DatetimeTooltipItem(BaseTooltipItem):
    """Customize tooltips for datetime data in Chart.

    Define specifications for a datetime item within a tooltip for a
    Chart widget to customize the appearance and content
    of tooltips displayed for datetime data.
    """

    @type_check
    def __init__(
        self,
        *,
        data_column: TemplatedStringItem,
        formatting: Optional[DateTimeFormatting] = None,
        label: Optional[Union[str, DataField]] = None,
    ) -> None:
        """Constructor for DatetimeTooltipItem.

        Args:
            data_column (TemplatedStringItem): name of column in pandas dataframe(s)
                used for the value of the tooltip item.
            formatting (DateTimeFormatting): tooltip formatting spec
                Defaults to DateTimeFormatting for Dates (i.e. not include HH:MM).
            label (Optional[Union[str, DataField]]): label to be used for tooltip item,
                it can be either a string or a DataField object.
        """
        super().__init__(
            data_column=data_column,
            formatting=formatting if formatting is not None else DateTimeFormatting(),
            label=label,
        )
