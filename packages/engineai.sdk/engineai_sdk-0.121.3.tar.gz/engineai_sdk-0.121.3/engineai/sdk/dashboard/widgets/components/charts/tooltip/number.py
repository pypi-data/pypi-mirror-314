"""Specs for number item for a tooltip."""

from typing import Optional
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting import NumberFormatting
from engineai.sdk.dashboard.templated_string import DataField
from engineai.sdk.dashboard.templated_string import TemplatedStringItem

from .base import BaseTooltipItem


class NumberTooltipItem(BaseTooltipItem):
    """Customize tooltips for numerical data in Chart.

    Define specifications for a number item within a tooltip for a Chart
    widget to customize the appearance and content of tooltips displayed
    for numerical data.
    """

    @type_check
    def __init__(
        self,
        *,
        data_column: TemplatedStringItem,
        formatting: Optional[NumberFormatting] = None,
        label: Optional[Union[str, DataField]] = None,
    ) -> None:
        """Constructor for NumberTooltipItem.

        Args:
            data_column: name of column in pandas dataframe(s) used for the value of
                the tooltip item.
            formatting: tooltip formatting spec.
                Defaults to None (Base NumberFormatting).
            label: label to be used for tooltip item, it can be either a string or a
                DataField object.
        """
        super().__init__(
            data_column=data_column,
            formatting=formatting if formatting is not None else NumberFormatting(),
            label=label,
        )
