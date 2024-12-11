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
from engineai.sdk.dashboard.widgets.components.charts.band.styling import (
    AxisBandStyling,
)
from engineai.sdk.dashboard.widgets.components.charts.exceptions import (
    ChartNoDataColumnError,
)
from engineai.sdk.dashboard.widgets.utils import build_data

from ..axis.label import AxisLabel


class AxisBand(DependencyManager):
    """Spec for Axis Band."""

    _DEPENDENCY_ID = "__AXIS_BAND_DEPENDENCY__"
    _ID_COUNTER = 0

    @type_check
    def __init__(
        self,
        data: Union[DataSource, pd.DataFrame, Http],
        *,
        from_column: str,
        to_column: str,
        label: Optional[Union[str, AxisLabel]] = None,
        styling: Optional[Union[Palette, AxisBandStyling]] = None,
    ) -> None:
        """Construct a plot line for an axis.

        Args:
            data: data source for the Axis Band.
            from_column: name of column in pandas dataframe(s) used for the
                start value for the band.
            to_column: name of column in pandas dataframe(s) used for the
                end value for the band.
            label: label annotation.
            styling: specs for chart band styling.
        """
        super().__init__(data=data, base_path=self.__generate_id())
        self.__from_column = from_column
        self.__to_column = to_column
        self.__styling = (
            AxisBandStyling(color_spec=styling)
            if isinstance(styling, Palette)
            else (
                AxisBandStyling(color_spec=Palette.PEACOCK_GREEN)
                if styling is None
                else styling
            )
        )
        self.__label = label if isinstance(label, AxisLabel) else AxisLabel(text=label)

    @property
    def data_id(self) -> str:
        """Get data id."""
        return "bands"

    def __generate_id(self) -> str:
        self._increment_id_counter()
        return f"bands_{self._ID_COUNTER}"

    @classmethod
    def _increment_id_counter(cls) -> None:
        cls._ID_COUNTER = cls._ID_COUNTER + 1

    def validate(self, data: pd.DataFrame, **_: Any) -> None:
        """Validates widget spec.

        Args:
            data: pandas DataFrame where the data is present.
        """
        if self.__from_column not in data.columns:
            raise ChartNoDataColumnError(
                data_column=self.__from_column,
            )
        if self.__to_column not in data.columns:
            raise ChartNoDataColumnError(
                data_column=self.__to_column,
            )
        self.__label.validate(data=data)

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "data": build_data(path=self.dependency_id),
            "fromKey": self.__from_column,
            "toKey": self.__to_column,
            "styling": self.__styling.build(),
            "label": self.__label.build(),
        }
