"""Spec for Tile Base Item."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting.datetime import DateTimeFormatting
from engineai.sdk.dashboard.formatting.number import NumberFormatting
from engineai.sdk.dashboard.formatting.text import TextFormatting
from engineai.sdk.dashboard.links.abstract import AbstractFactoryLinkItemsHandler
from engineai.sdk.dashboard.templated_string import DataField
from engineai.sdk.dashboard.templated_string import InternalDataField
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings

from ..exceptions import TileValidateValueError

ItemFormatting = Union[TextFormatting, NumberFormatting, DateTimeFormatting]


class BaseTileContentItem(AbstractFactoryLinkItemsHandler):
    """Spec for Tile Base Content Item."""

    _INPUT_KEY: Optional[str] = None

    @type_check
    def __init__(
        self,
        *,
        data_column: TemplatedStringItem,
        formatting: ItemFormatting,
        label: Optional[Union[TemplatedStringItem, DataField]] = None,
        required: bool = True,
    ) -> None:
        """Construct spec for the TileItem class.

        Args:
            data_column: key in data that will have the values used by the item.
            formatting: formatting spec.
            label: str that will label the item values.
            required: Flag to make Number item mandatory. If required is True
                and no Data the widget will show an error. If
                required is False and no Data, the item is not shown.
        """
        super().__init__()
        self._data_column = data_column
        self._formatting = formatting
        self._required = required

        self.__set_label(label=label)

    @property
    def input_key(self) -> str:
        """Input key for the item."""
        if self._INPUT_KEY is None:
            msg = "You must define a class attribute `_INPUT_KEY` in your subclass."
            raise NotImplementedError(msg)
        return self._INPUT_KEY

    def __set_label(
        self, label: Optional[Union[TemplatedStringItem, DataField]]
    ) -> None:
        if label is None:
            self._label = InternalDataField()
        elif isinstance(label, (DataField)):
            self._label = InternalDataField(label)
        else:
            self._label = InternalDataField(str(label))

    def validate(self, data: Dict[str, Any]) -> None:
        """Validates Tile Content Item.

        Args:
            widget_id (str): id of Tile Widget.
            data (Dict[str, Any]): data inside `path`.

        Raises:
            TileValidateValueError if `value_key` not in data.
        """
        if self._required:
            if self._data_column is not None and str(self._data_column) not in data:
                raise TileValidateValueError(
                    subclass="TileItem",
                    argument="value_key",
                    value=str(self._data_column),
                )
            self._label.validate(data=data)

    def _build_extra_inputs(self) -> Dict[str, Any]:
        """Abstract method for build extra input."""
        return {}

    def build_item(self) -> Dict[str, Any]:
        """Builds item spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            self.input_key: self.build(),
        }

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "valueKey": build_templated_strings(items=self._data_column),
            "formatting": self._formatting.build(),
            "label": self._label.build() if self._label else "",
            "required": self._required,
            **self._build_extra_inputs(),
        }
