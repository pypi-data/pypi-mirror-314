"""Spec for Tile Date Item."""

from typing import Optional
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting.datetime import DateTimeFormatting
from engineai.sdk.dashboard.templated_string import DataField
from engineai.sdk.dashboard.templated_string import TemplatedStringItem

from ..base import BaseTileContentItem


class DateItem(BaseTileContentItem):
    """Spec for Tile Date Item."""

    _INPUT_KEY = "date"

    @type_check
    def __init__(
        self,
        *,
        data_column: TemplatedStringItem,
        formatting: Optional[DateTimeFormatting] = None,
        label: Optional[Union[TemplatedStringItem, DataField]] = None,
        required: bool = True,
    ) -> None:
        """Construct spec for the Tile Date Item class.

        Args:
            data_column: key in data that will have the values used by the item.
            formatting: formatting spec.
            label: str that will label the item values.
            required: Flag to make Number item mandatory. If required is True
                and no Data the widget will show an error. If
                required is False and no Data, the item is not shown.
        """
        super().__init__(
            data_column=data_column,
            formatting=formatting if formatting is not None else DateTimeFormatting(),
            label=label,
            required=required,
        )
