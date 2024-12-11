"""Spec for Tile Matrix Base Item."""

from typing import Any
from typing import Dict
from typing import Generic
from typing import Optional
from typing import TypeVar
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting.number import NumberFormatting
from engineai.sdk.dashboard.formatting.text import TextFormatting
from engineai.sdk.dashboard.templated_string import DataField
from engineai.sdk.dashboard.templated_string import InternalDataField
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.tile_matrix.exceptions import (
    TileMatrixValidateValueError,
)

from .chart.chart_typing import TileMatrixChartStyling
from .number.typing import TileMatrixNumberItemStyling
from .text.typing import TileMatrixTextItemStyling
from .typing import Actions

ItemFormatting = Union[TextFormatting, NumberFormatting]
TileMatrixItemStyling = Union[
    TileMatrixNumberItemStyling,
    TileMatrixTextItemStyling,
    TileMatrixChartStyling,
]

Styling = TypeVar("Styling", bound=TileMatrixItemStyling)


class BaseTileMatrixItem(AbstractFactory, Generic[Styling]):
    """Spec for Base Tile Matrix Item."""

    _INPUT_KEY: Optional[str] = None

    @type_check
    def __init__(
        self,
        *,
        data_column: TemplatedStringItem,
        label: Optional[Union[TemplatedStringItem, DataField]] = None,
        icon: Optional[Union[TemplatedStringItem, DataField]] = None,
        link: Optional[Actions] = None,
        formatting: Optional[ItemFormatting] = None,
        styling: Optional[Styling] = None,
        required: bool = True,
    ) -> None:
        """Construct spec for the BaseTileMatrixItem class.

        Args:
            data_column: column that has the value to be represented.
            label: Label text to be displayed.
            icon: icon to be displayed.
            link: link or action to be executed in the URL Icon.
            formatting: formatting spec.
            styling: styling spec.
            required: Flag to make Number item mandatory.
        """
        super().__init__()
        self._data_column = data_column
        self._link = link
        self._formatting = formatting
        self._styling = styling
        self._required = required

        self._label = self.__set_parameter(label)
        self._icon = self.__set_parameter(icon)

    @property
    def input_key(self) -> str:
        """Returns input key."""
        if self._INPUT_KEY is None:
            msg = "INPUT_KEY must be implemented in the subclass of BaseTileMatrixItem."
            raise NotImplementedError(msg)
        return self._INPUT_KEY

    def __set_parameter(
        self, parameter: Optional[Union[TemplatedStringItem, DataField]]
    ) -> InternalDataField:
        if parameter is None:
            return InternalDataField()
        if isinstance(parameter, DataField):
            return InternalDataField(parameter)
        return InternalDataField(str(parameter))

    def prepare(self) -> None:
        """Prepare Tile Matrix Item."""
        if self._styling is not None:
            self._styling.prepare(self._data_column)

    def validate(
        self,
        *,
        data: pd.DataFrame,
    ) -> None:
        """Validates Tile Matrix item.

        Args:.
            data (pd.DataFrame): data inside `path`.
        """
        if self._required:
            if str(self._data_column) not in data:
                raise TileMatrixValidateValueError(
                    subclass="TileMatrixItem",
                    argument="value_key",
                    value=str(self._data_column),
                )

            self._label.validate(data)

            if self._icon is not None:
                self._icon.validate(data)

            if self._link is not None:
                self._link.validate(
                    data=data,
                    widget_class=self.__class__.__name__,
                    warnings_flag=True,
                )

    def _build_extra_inputs(self) -> Dict[str, Any]:
        """Abstract method for build extra input."""
        return {}

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "valueKey": build_templated_strings(items=self._data_column),
            "label": self._label.build(),
            "icon": self._icon.build() if self._icon else None,
            "formatting": self._formatting.build() if self._formatting else None,
            "link": self._link.build_action() if self._link else None,
            **self._build_extra_inputs(),
        }
