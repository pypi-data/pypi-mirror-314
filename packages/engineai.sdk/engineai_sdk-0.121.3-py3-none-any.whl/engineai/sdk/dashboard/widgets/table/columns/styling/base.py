"""Specification for Table Column Styling Base class."""

from typing import Any
from typing import Dict
from typing import Mapping
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.links.abstract import AbstractFactoryLinkItemsHandler
from engineai.sdk.dashboard.styling.color import DiscreteMap
from engineai.sdk.dashboard.styling.color import Gradient
from engineai.sdk.dashboard.styling.color.spec import build_color_spec
from engineai.sdk.dashboard.styling.color.typing import ColorSpec
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.table.columns.styling.exceptions import (
    TableColumnStylingValidationError,
)
from engineai.sdk.dashboard.widgets.table.columns.styling.exceptions import (
    TableColumnStylingValueError,
)


class TableColumnStylingBase(AbstractFactoryLinkItemsHandler):
    """Specification for Table Column Styling Base class."""

    _API_DATA_KEY: Optional[str] = "dataKey"

    @type_check
    def __init__(
        self,
        *,
        color_spec: Optional[ColorSpec] = None,
        data_column: Optional[Union[str, WidgetField]] = None,
    ) -> None:
        """Construct for TableColumnStylingBase class.

        Args:
            data_column: id of column which values are used for chart. By default,
                will use values of column to which styling is applied.
            color_spec: spec for color class.
        """
        super().__init__()
        self._data_column = data_column
        self.__color_spec = color_spec

    @property
    def color_spec(self) -> Optional[ColorSpec]:
        """Return color spec."""
        return self.__color_spec

    def _build_extra_inputs(self) -> Dict[str, Any]:
        return {}

    def _build_color_spec(self) -> Dict[str, Any]:
        return (
            {"colorSpec": build_color_spec(spec=self.__color_spec)}
            if self.__color_spec is not None
            else {}
        )

    @property
    def data_column(
        self,
    ) -> Optional[Union[str, WidgetField]]:
        """Name of column used in pandas dataframe.

        Returns None if a single color is used.

        Returns:
            Optional[Union[str, WidgetField]]: data column
        """
        return self._data_column

    def prepare(self, data_column: Optional[Union[str, WidgetField]]) -> None:
        """Prepare data column."""
        if (
            isinstance(self.__color_spec, (DiscreteMap, Gradient))
            and self._data_column is None
        ):
            self._data_column = data_column

    def validate(self, *, data: Union[pd.DataFrame, Dict[str, Any]]) -> None:
        """Validate if dataframe that will be used for column contains required columns.

        Args:
            data: pandas dataframe which will be used for table.

        Raises:
            ValueError: if data does not contain data_column for TableColumn
        """
        if (
            self.__color_spec is not None
            and not self._data_column
            and isinstance(self.__color_spec, (DiscreteMap, Gradient))
        ):
            raise TableColumnStylingValueError(_class=self.__class__.__name__)

        if self._data_column is not None and (
            (isinstance(data, pd.DataFrame) and self.data_column not in data.columns)
            or (isinstance(data, dict) and self.data_column not in data)
        ):
            raise TableColumnStylingValidationError(
                class_name=self.__class__.__name__,
                data_column=f"{self.data_column}",
            )

    def _build_key_input(self) -> Mapping[str, Any]:
        return {
            self._API_DATA_KEY: build_templated_strings(items=self._data_column or " ")
        }

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            **self._build_key_input(),
            **self._build_color_spec(),
            **self._build_extra_inputs(),
        }


class TableSparklineColumnStylingBase(TableColumnStylingBase):
    """Specification for Table Sparkline Column Styling Base class."""

    _API_DATA_KEY: Optional[str] = "valueKey"
