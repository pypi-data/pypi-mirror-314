"""Spec for Axis Line."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.data.decorator import DataSource
from engineai.sdk.dashboard.data.http import Http
from engineai.sdk.dashboard.data.manager.manager import DependencyManager
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.styling.color import Palette
from engineai.sdk.dashboard.widgets.components.charts.exceptions import (
    ChartNoDataColumnError,
)
from engineai.sdk.dashboard.widgets.components.charts.styling.enums import DashStyle
from engineai.sdk.dashboard.widgets.utils import build_data

from ..axis.label import AxisLabel
from .styling import AxisLineStyling


class AxisLine(DependencyManager):
    """Spec for Axis Line."""

    _DEPENDENCY_ID = "__AXIS_LINE_DEPENDENCY__"
    _ID_COUNTER = 0

    @type_check
    def __init__(
        self,
        data: Union[DataSource, pd.DataFrame, Http],
        *,
        data_column: str,
        label: Optional[Union[str, AxisLabel]] = None,
        styling: Optional[Union[Palette, AxisLineStyling]] = None,
        dash_style: DashStyle = DashStyle.DASH,
    ) -> None:
        """Construct a plot line for an axis.

        Args:
            data: data source for the Axis line.
            data_column: name of column in pandas dataframe(s) used for the
                value of axis line
            label: label annotation.
            styling: specs for chart band styling.
            dash_style: line dash style.
        """
        super().__init__(data=data, base_path=self.__generate_id())
        self.__data_column = data_column
        self.__styling = (
            AxisLineStyling(color_spec=styling)
            if isinstance(styling, Palette)
            else (
                AxisLineStyling(color_spec=Palette.PEACOCK_GREEN)
                if styling is None
                else styling
            )
        )

        self.__label = label if isinstance(label, AxisLabel) else AxisLabel(text=label)
        self.__dash_style = dash_style

    @property
    def data_id(self) -> str:
        """Get data id."""
        return "lines"

    def __generate_id(self) -> str:
        self._increment_id_counter()
        return f"lines_{self._ID_COUNTER}"

    @classmethod
    def _increment_id_counter(cls) -> None:
        cls._ID_COUNTER = cls._ID_COUNTER + 1

    def validate(self, data: pd.DataFrame, **_: Any) -> None:
        """Validates widget spec.

        Args:
            data: pandas DataFrame where the data is present.
        """
        if self.__data_column not in data.columns:
            raise ChartNoDataColumnError(
                data_column=self.__data_column,
            )
        self.__label.validate(data=data)

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "valueKey": self.__data_column,
            "styling": self.__styling.build(),
            "dashStyle": self.__dash_style.value,
            "label": self.__label.build(),
            "data": build_data(path=self.dependency_id),
        }
