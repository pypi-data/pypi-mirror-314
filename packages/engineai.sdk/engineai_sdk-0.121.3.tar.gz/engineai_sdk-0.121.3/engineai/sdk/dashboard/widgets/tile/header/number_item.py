"""Spec for Tile Header Number Item."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting.number import NumberFormatting
from engineai.sdk.dashboard.links.abstract import AbstractFactoryLinkItemsHandler
from engineai.sdk.dashboard.templated_string import DataField
from engineai.sdk.dashboard.templated_string import InternalDataField
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.items.styling import NumberStylingChip
from engineai.sdk.dashboard.widgets.components.items.styling import NumberStylingDot
from engineai.sdk.dashboard.widgets.components.items.styling import NumberStylingFont

from ..content.exceptions import TileValidateValueError

TileHeaderNumberStyling = Union[
    NumberStylingChip,
    NumberStylingDot,
    NumberStylingFont,
]


class HeaderNumberItem(AbstractFactoryLinkItemsHandler):
    """Spec for Tile Header Number Item."""

    @type_check
    def __init__(
        self,
        *,
        value_key: TemplatedStringItem,
        formatting: Optional[NumberFormatting] = None,
        label: Optional[Union[TemplatedStringItem, DataField]] = None,
        styling: Optional[TileHeaderNumberStyling] = None,
    ) -> None:
        """Construct spec for the Tile Header Number Item class.

        Args:
            value_key: key in data that will have the values used by the item.
            formatting: formatting spec.
            label: label the item values.
            styling: styling spec for number header item.
        """
        super().__init__()
        self._value_key = value_key
        self._formatting = formatting if formatting is not None else NumberFormatting()
        self.__styling = styling

        self.__set_label(label=label)

    def __set_label(
        self, label: Optional[Union[TemplatedStringItem, DataField]]
    ) -> None:
        if label is None:
            self._label = InternalDataField()
        elif isinstance(label, (DataField)):
            self._label = InternalDataField(label)
        else:
            self._label = InternalDataField(DataField(str(label), ""))

    def validate(
        self,
        data: Dict[str, Any],
    ) -> None:
        """Validates Tile Content Item.

        Args:
            widget_id (str): id of Tile Widget.
            data (Dict[str, Any]): data inside `path`.
            path (List[str]): path to data in storage.

        Raises:
            TileValidateValueError if `value_key` not in data.
        """
        if self._value_key is not None and str(self._value_key) not in data:
            raise TileValidateValueError(
                subclass="TileItem",
                argument="value_key",
                value=str(self._value_key),
            )

        if self.__styling is not None:
            self.__styling.validate(
                data=data,
                column_name="data_key",
            )

        self._label.validate(data=data)

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "valueKey": build_templated_strings(items=self._value_key),
            "formatting": self._formatting.build(),
            "label": self._label.build(),
            "styling": self.__styling.build_styling()
            if self.__styling is not None
            else None,
        }
