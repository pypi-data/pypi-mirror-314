"""Spec for a column series of a Timeseries widget."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.links.typing import GenericLink
from engineai.sdk.dashboard.styling.color import Palette
from engineai.sdk.dashboard.widgets.components.charts.series.entities.country import (
    CountryEntity,
)
from engineai.sdk.dashboard.widgets.components.charts.series.entities.typing import (
    Entities,
)
from engineai.sdk.dashboard.widgets.components.charts.styling import ColumnSeriesStyling
from engineai.sdk.dashboard.widgets.components.charts.typing import TooltipItems

from .base import TimeseriesBaseSeries


class ColumnSeries(TimeseriesBaseSeries):
    """Visualize data as vertical columns in Timeseries widget.

    Construct specifications for a column series within a Timeseries widget to
    visualize data as vertical columns on the chart. Each column represents a
    distinct data point, with the height of the column reflecting its
    corresponding value.
    """

    _INPUT_KEY = "column"
    _styling_class = ColumnSeriesStyling

    @type_check
    def __init__(
        self,
        *,
        data_column: Union[str, WidgetField],
        name: Optional[Union[str, GenericLink]] = None,
        styling: Optional[Union[Palette, ColumnSeriesStyling]] = None,
        entity: Optional[Entities] = None,
        show_in_legend: bool = True,
        required: bool = True,
        visible: bool = True,
        right_axis: bool = False,
        tooltips: Optional[TooltipItems] = None,
    ) -> None:
        """Constructor for ColumnSeries.

        Args:
            data_column: name of column in pandas dataframe(s) used for the values of
                this series.
            name: series name (shown in legend and tooltip).
            styling: styling spec, by default uses the values from the sequential
                palette.
            entity: entity spec.
            show_in_legend: whether to show series in legend or not.
            required: Flag to make the Series mandatory. If required == True and no
                Data the widget will show an error. If required==False and no Data,
                the widget hides the Series.
            visible: Flag to make the Series visible when chart is loaded.
            right_axis: Flag to make the Series visible on the right axis.
            tooltips: tooltip items to be displayed at Series level.
        """
        super().__init__(
            name=name,
            data_column=data_column,
            show_in_legend=show_in_legend,
            required=required,
            visible=visible,
            styling=(
                ColumnSeriesStyling(color_spec=styling)
                if isinstance(styling, Palette)
                else styling
            ),
            entity=entity,
            right_axis=right_axis,
            tooltips=tooltips,
        )

    def validate(self, *, data: pd.DataFrame) -> None:
        """Validate if dataframe that will be used for series contains required columns.

        Args:
            data: pandas dataframe which will be used for table
        """
        super().validate(data=data)

        if self._entity is not None and isinstance(self._entity, CountryEntity):
            self._entity.validate_country_code()

    def _build_extra_inputs(self) -> Dict[str, Any]:
        return {
            "transforms": [transform.build() for transform in self._transforms],
        }
