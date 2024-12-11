"""Base Tooltip Item class."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting import DateTimeFormatting
from engineai.sdk.dashboard.formatting import MapperFormatting
from engineai.sdk.dashboard.formatting import NumberFormatting
from engineai.sdk.dashboard.formatting import TextFormatting
from engineai.sdk.dashboard.links.abstract import AbstractFactoryLinkItemsHandler
from engineai.sdk.dashboard.templated_string import DataField
from engineai.sdk.dashboard.templated_string import InternalDataField
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings

from .exceptions import TooltipItemColumnNotFoundError

TooltipItemFormatter = Union[
    MapperFormatting, NumberFormatting, TextFormatting, DateTimeFormatting
]


class BaseTooltipItem(AbstractFactoryLinkItemsHandler):
    """Base Tooltip Item class."""

    @type_check
    def __init__(
        self,
        *,
        data_column: TemplatedStringItem,
        formatting: TooltipItemFormatter,
        label: Optional[Union[str, DataField]] = None,
    ) -> None:
        """Construct for BaseTooltipItem class.

        Args:
            data_column (TemplatedStringItem): name of column in pandas dataframe(s)
                used for the value of the tooltip item.
            formatting (TooltipItemFormatter): tooltip formatting spec.
            label (Optional[Union[str, DataField]]): label to be used for tooltip item,
                it can be either a string or a DataField object.
        """
        super().__init__()
        self.__label = InternalDataField(
            label or self.__reformat_data_column(str(data_column))
        )
        self.__data_column = data_column
        self.__formatting = formatting

    def __hash__(self) -> int:
        return hash(
            f"{self.__data_column!s}_{self.__label._value!s}_{self.__label._value_key!s}"
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and (
            self.__label._value == other.__label._value
            and self.__label._value_key == other.__label._value_key
            and self.data_column == other.data_column
        )

    @property
    def label(self) -> InternalDataField:
        """Get label."""
        return self.__label

    @property
    def data_column(self) -> TemplatedStringItem:
        """Get data column."""
        return self.__data_column

    def __reformat_data_column(self, data_column: str) -> str:
        return data_column.replace("_", " ").title()

    def validate(self, *, data: pd.DataFrame) -> None:
        """Validate if dataframe that will be used for column contains required columns.

        Args:
            data (DataFrame): pandas dataframe which will be used for table

        Raises:
            TooltipItemColumnNotFoundError: if a specific column does not exists in data
        """
        self.__label.validate(data)

        if self.__data_column not in data.columns:
            raise TooltipItemColumnNotFoundError(
                class_name=self.__class__.__name__,
                column_name="data_column",
                column_value=self.__data_column,
            )
        if isinstance(self.__formatting, NumberFormatting):
            self.__formatting.validate(data)

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "label": self.__label.build(),
            "valueKey": build_templated_strings(items=self.__data_column),
            "formatting": self.__formatting.build(),
        }
