"""Spec for Tile Number Item."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting.number import NumberFormatting
from engineai.sdk.dashboard.templated_string import DataField
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.widgets.components.items.styling import NumberStylingArrow
from engineai.sdk.dashboard.widgets.components.items.styling import NumberStylingChip
from engineai.sdk.dashboard.widgets.components.items.styling import NumberStylingDot
from engineai.sdk.dashboard.widgets.components.items.styling import NumberStylingFont

from ..base import BaseTileContentItem

TileNumberStyling = Union[
    NumberStylingArrow,
    NumberStylingChip,
    NumberStylingDot,
    NumberStylingFont,
]


class NumberItem(BaseTileContentItem):
    """Spec for Tile Number Item."""

    _INPUT_KEY = "number"

    @type_check
    def __init__(
        self,
        *,
        data_column: TemplatedStringItem,
        formatting: Optional[NumberFormatting] = None,
        label: Optional[Union[TemplatedStringItem, DataField]] = None,
        required: bool = True,
        styling: Optional[TileNumberStyling] = None,
    ) -> None:
        """Construct spec for the Tile Number Item class.

        Args:
            data_column: key in data that will have the values used by the item.
            formatting: formatting spec.
            label: str that will label the item values.
            required: Flag to make Number item mandatory. If required is True
                and no Data the widget will show an error. If
                required is False and no Data, the item is not shown.
            styling: styling spec for number item.
        """
        super().__init__(
            data_column=data_column,
            formatting=formatting if formatting is not None else NumberFormatting(),
            label=label,
            required=required,
        )
        self.__styling = styling

    def _build_extra_inputs(self) -> Dict[str, Any]:
        if self.__styling is not None:
            return {"styling": self.__styling.build_styling()}
        return {}

    def validate(self, data: Dict[str, Any]) -> None:
        """Validates Tile Number Item.

        Args:
            widget_id (str): id of Tile Widget.
            data (Dict[str, Any]): Dict where the data is present.

        Raises:
            TileValidateValueError if `value_key` not in data.
        """
        if self._required:
            super().validate(data=data)
            if self.__styling is not None:
                self.__styling.validate(
                    data=data,
                    column_name="data_key",
                )
