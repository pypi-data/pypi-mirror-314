"""Specs for Base Search Result Column."""

from typing import Any
from typing import Dict
from typing import Mapping
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.styling.color import Palette
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.search.exceptions import (
    SearchValidateNoDataColumnError,
)

from .styling.base_styling import ResultColumnStyling


class BaseResultItem(AbstractFactory):
    """Specs for Base Search Result Column."""

    def __init__(
        self,
        data_column: TemplatedStringItem,
        styling: Optional[Union[Palette, ResultColumnStyling]] = None,
    ) -> None:
        """Constructor for Base Search Result Column.

        Args:
            data_column: Column name in pandas DataFrame used for
                search result.
            styling: Specs for Search Result styling.

        """
        self._data_column = data_column
        self.__styling = (
            ResultColumnStyling(color_spec=styling)
            if isinstance(styling, Palette)
            else styling
        )

    def _build_extra_inputs(self) -> Mapping[str, Any]:
        """Method used to build extra fields."""
        return {}

    def validate(self, *, data: pd.DataFrame) -> None:
        """Validate if data has the right columns.

        Args:
            data: pandas DataFrame where the data is present.

        Raises:
            SearchValidateNoDataColumnError: if data does not contain data_column
        """
        if isinstance(self._data_column, str) and self._data_column not in data.columns:
            raise SearchValidateNoDataColumnError(data_column=self._data_column)

        if self.__styling is not None:
            self.__styling.validate(data=data)

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "dataKey": build_templated_strings(items=self._data_column),
            "styling": self.__styling.build() if self.__styling is not None else None,
            **self._build_extra_inputs(),
        }
