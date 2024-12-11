"""Spec for Search Widget Result Column Style."""

from typing import Any
from typing import Dict
from typing import Optional

import pandas as pd

from engineai.sdk.dashboard.styling.color.discrete_map import DiscreteMap
from engineai.sdk.dashboard.styling.color.gradient import Gradient
from engineai.sdk.dashboard.styling.color.palette import Palette
from engineai.sdk.dashboard.styling.color.spec import build_color_spec
from engineai.sdk.dashboard.styling.color.typing import ColorSpec
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.search.exceptions import (
    SearchStylingMissingDataColumnError,
)
from engineai.sdk.dashboard.widgets.search.exceptions import (
    SearchValidateNoDataColumnError,
)


class ResultColumnStyling:
    """Spec for Search Widget Result Column Style."""

    def __init__(
        self,
        *,
        color_spec: Optional[ColorSpec] = None,
        data_column: Optional[TemplatedStringItem] = None,
    ) -> None:
        """Construct for Search Widget Result Column Style.

        Args:
            color_spec: Spec for coloring columns.
            data_column: Name of column in pandas
                dataframe(s) used for color spec if a gradient is used. Optional for
                single colors.
        """
        super().__init__()
        if (
            color_spec is not None
            and isinstance(color_spec, (DiscreteMap, Gradient))
            and data_column is None
        ):
            raise SearchStylingMissingDataColumnError
        self.__color_spec = color_spec or Palette.AQUA_GREEN
        self.__data_column = data_column

    def validate(
        self,
        *,
        data: pd.DataFrame,
    ) -> None:
        """Validate if data has the right columns.

        Args:
            data: pandas dataframe which will be used for table.

        Raises:
            SearchValidateNoDataColumnError: if data does not contain data_column
        """
        if (
            isinstance(self.__data_column, str)
            and self.__data_column not in data.columns
        ):
            raise SearchValidateNoDataColumnError(data_column=self.__data_column)

        # TODO: Validate abstractLinks if used (widgetField, f.e)

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "chip": {
                "colorSpec": (
                    build_color_spec(spec=self.__color_spec)
                    if self.__color_spec
                    else None
                ),
                "dataKey": build_templated_strings(items=self.__data_column),
            }
        }
