"""Spec for a area range series of a Timeseries widget."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.links.typing import GenericLink
from engineai.sdk.dashboard.styling.color import Palette
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.charts.series.entities.country import (
    CountryEntity,
)
from engineai.sdk.dashboard.widgets.components.charts.series.entities.typing import (
    Entities,
)
from engineai.sdk.dashboard.widgets.components.charts.styling import (
    AreaRangeSeriesStyling,
)
from engineai.sdk.dashboard.widgets.components.charts.typing import TooltipItems

from .base import TimeseriesBaseSeries


class AreaRangeSeries(TimeseriesBaseSeries):
    """Visualize data as filled areas between low and high values.

    Construct specifications for an area range series within a Timeseries
    widget to visualize data as filled areas between low and high values on the chart.
    """

    _INPUT_KEY = "range"
    _styling_class = AreaRangeSeriesStyling

    @type_check
    def __init__(
        self,
        *,
        low_data_column: Union[str, WidgetField],
        high_data_column: Union[str, WidgetField],
        name: Union[str, GenericLink],
        styling: Optional[Union[Palette, AreaRangeSeriesStyling]] = None,
        entity: Optional[Entities] = None,
        show_in_legend: bool = True,
        required: bool = True,
        visible: bool = True,
        right_axis: bool = False,
        tooltips: Optional[TooltipItems] = None,
    ) -> None:
        """Constructor for AreaRangeSeries.

        Args:
            low_data_column: name of column in pandas dataframe(s) used for the low
                values of this series.
            high_data_column: name of column in pandas dataframe(s) used for the high
                values of this series.
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
            data_column=None,
            show_in_legend=show_in_legend,
            required=required,
            visible=visible,
            styling=(
                AreaRangeSeriesStyling(color_spec=styling)
                if isinstance(styling, Palette)
                else styling
            ),
            entity=entity,
            right_axis=right_axis,
            tooltips=tooltips,
        )
        self._low_data_column: Union[str, WidgetField] = (
            low_data_column if isinstance(low_data_column, str) else low_data_column
        )
        self._high_data_column: Union[str, WidgetField] = (
            high_data_column if isinstance(high_data_column, str) else high_data_column
        )

    def validate(self, *, data: pd.DataFrame) -> None:
        """Validate if dataframe that will be used for series contains required columns.

        Args:
            data: pandas dataframe which will be used for table
        """
        super().validate(data=data)

        super()._validate_data_column(
            data=data,
            data_column=self._low_data_column,
            data_column_name="low_data_column",
        )

        super()._validate_data_column(
            data=data,
            data_column=self._high_data_column,
            data_column_name="high_data_column",
        )

        if self._entity is not None and isinstance(self._entity, CountryEntity):
            self._entity.validate_country_code()

    def _build_extra_inputs(self) -> Dict[str, Any]:
        return {
            "lowKey": build_templated_strings(items=self._low_data_column),
            "highKey": build_templated_strings(items=self._high_data_column),
            "lowTransforms": [transform.build() for transform in self._transforms],
            "highTransforms": [transform.build() for transform in self._transforms],
        }
