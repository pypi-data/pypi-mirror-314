"""Spec for Pie Chart."""

from typing import Any
from typing import Dict
from typing import Optional

import pandas as pd

from engineai.sdk.dashboard.base import AbstractFactory
from engineai.sdk.dashboard.widgets.components.charts.typing import TooltipItems

from .series.typings import ChartSeries
from .tooltip import Tooltip


class Chart(AbstractFactory):
    """Spec for Pie Chart."""

    def __init__(
        self,
        series: ChartSeries,
        tooltips: Optional[TooltipItems] = None,
    ) -> None:
        """Constructor for Pie Chart.

        Args:
            series: spec for series.
            tooltips: tooltip items to be displayed at Chart level.
        """
        self._series = series
        self._tooltip = Tooltip(
            category_column=series.category_column,
            tooltips=tooltips,
        )

    def prepare(self, dependency_id: str, json_data: Any = None) -> None:
        """Prepare Widget Spec to be validated."""
        self._series.prepare(dependency_id=dependency_id, json_data=json_data)
        self._tooltip.prepare(dependency_id=dependency_id, json_data=json_data)

    def validate(self, *, data: pd.DataFrame) -> None:
        """Validates Pie Series Widget and the inner components specs.

        Raises:
            PieValidateValueError if `data_column`, `category_column`, not in data.
            ChartStylingNoDataColumnError if data_column is provided in styling and
                not in data.
        """
        self._series.validate(
            data=data,
        )
        self._tooltip.validate(data=data)

    def build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API.

        Returns:
            Input object for Dashboard API
        """
        return {
            "series": self._series.build(),
            "tooltip": self._tooltip.build() if self._tooltip else None,
        }
