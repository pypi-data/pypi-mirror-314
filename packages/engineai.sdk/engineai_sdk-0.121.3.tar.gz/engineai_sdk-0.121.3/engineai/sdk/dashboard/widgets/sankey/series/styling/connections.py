"""Spec to style connections in a Sankey widget."""

from typing import Any
from typing import Dict
from typing import Optional

import pandas as pd

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.styling import color
from engineai.sdk.dashboard.styling.color import DiscreteMap
from engineai.sdk.dashboard.styling.color import Gradient
from engineai.sdk.dashboard.styling.color.spec import build_color_spec
from engineai.sdk.dashboard.styling.color.typing import ColorSpec
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.sankey.exceptions import (
    SankeyDataColumnMissingError,
)
from engineai.sdk.dashboard.widgets.sankey.exceptions import (
    SankeyItemsValidateNoDataColumnError,
)


class ConnectionsStyling(AbstractFactory):
    """Spec to style connections in a Sankey widget."""

    @type_check
    def __init__(
        self,
        *,
        color_spec: Optional[ColorSpec] = None,
        data_column: Optional[TemplatedStringItem] = None,
    ) -> None:
        """Construct style spec for a node.

        Args:
            color_spec: spec for coloring a node.
            data_column: name of column in pandas
                dataframe(s) used for color spec if a gradient is used.

        Raises:
            SankeyDataColumnMissingError: if color_spec is
                DiscreteMap/Gradient and data_column has not been specified
        """
        super().__init__()
        if not data_column and isinstance(color_spec, (DiscreteMap, Gradient)):
            raise SankeyDataColumnMissingError(
                widget_id=None, color_specs=["DiscreteMap", "Gradient"]
            )
        self.__color_spec = color_spec if color_spec else color.Palette.MINT_GREEN
        self.__data_column = data_column

    def validate(self, *, data: pd.DataFrame) -> None:
        """Validates Sankey Series Connections Styling widget spec.

        Args:
            data: Data related to Connections

        Raises:
            SankeyItemsValidateNoDataColumnError: If data_column is not found in
                Data Columns
        """
        if (
            self.__data_column
            and isinstance(data, pd.DataFrame)
            and self.__data_column not in data.columns
        ):
            raise SankeyItemsValidateNoDataColumnError(
                missing_column_name="Data column",
                missing_column=self.__data_column,
                item_name="Connection",
                style=True,
            )

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "colorSpec": build_color_spec(spec=self.__color_spec),
            "valueKey": build_templated_strings(
                items=self.__data_column if self.__data_column else " "
            ),
        }
