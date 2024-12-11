"""Spec for Base Tile Matrix Chart Items."""

from typing import Any
from typing import Dict

import pandas as pd

from engineai.sdk.dashboard.templated_string import build_templated_strings

from ..base import BaseTileMatrixItem
from .chart_typing import TileMatrixChartStyling


class BaseTileMatrixChartItem(BaseTileMatrixItem[TileMatrixChartStyling]):
    """Spec for Base Tile Matrix Chart Items."""

    _INPUT_KEY = "chart"
    _API_CHART_TYPE: str = ""

    def prepare(self) -> None:
        """Prepares styling spec for dashboard API."""
        if self._styling is not None:
            self._styling.prepare(self._data_column)

    def _build_configuration(self) -> Dict[str, Any]:
        """Builds configuration spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            self._API_CHART_TYPE: self._build_chart(),
        }

    def _build_extra_chart_inputs(self) -> Dict[str, Any]:
        """Builds extra inputs for chart spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {}

    def _build_chart(self) -> Dict[str, Any]:
        """Builds chart spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "valueKey": build_templated_strings(items=self._data_column),
            "styling": self._styling.build() if self._styling else None,
            **self._build_extra_chart_inputs(),
        }

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "label": self._label.build(),
            "icon": self._icon.build() if self._icon else None,
            "formatting": self._formatting.build() if self._formatting else None,
            "link": self._link.build_action() if self._link else None,
            "configuration": self._build_configuration(),
        }

    def validate(
        self,
        *,
        data: pd.DataFrame,
    ) -> None:
        """Validates Tile Matrix Item.

        Args:
            data (pd.DataFrame): data inside `path`.
        """
        super().validate(
            data=data,
        )
        if self._styling is not None:
            self._styling.validate(
                data=data,
                column_name="value_column",
            )
