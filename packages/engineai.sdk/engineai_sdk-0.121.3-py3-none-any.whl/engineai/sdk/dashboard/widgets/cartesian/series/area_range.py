"""Spec for a area range series of a Cartesian widget."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting import NumberFormatting
from engineai.sdk.dashboard.links.typing import GenericLink
from engineai.sdk.dashboard.styling.color import Palette
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.charts.series.entities.typing import (
    Entities,
)
from engineai.sdk.dashboard.widgets.components.charts.styling import (
    AreaRangeSeriesStyling,
)
from engineai.sdk.dashboard.widgets.components.charts.typing import TooltipItems

from .base import CartesianBaseSeries


class AreaRangeSeries(CartesianBaseSeries):
    """Spec for a area range series of a Cartesian widget."""

    _INPUT_KEY = "areaRange"
    _styling_class = AreaRangeSeriesStyling

    @type_check
    def __init__(
        self,
        *,
        low_data_column: Union[str, GenericLink],
        high_data_column: Union[str, GenericLink],
        x_data_column: Optional[Union[str, GenericLink]] = None,
        formatting: Optional[NumberFormatting] = None,
        name: Union[str, GenericLink],
        styling: Optional[Union[Palette, AreaRangeSeriesStyling]] = None,
        entity: Optional[Entities] = None,
        show_in_legend: bool = True,
        required: bool = True,
        visible: bool = True,
        point_label_column: Optional[Union[str, GenericLink]] = None,
        tooltips: Optional[TooltipItems] = None,
    ) -> None:
        """Construct area range series.

        Args:
            low_data_column: name of column in pandas dataframe(s) used for the low
                values of this series.
            high_data_column: name of column in pandas dataframe(s) used for the high
                values of this series.
            x_data_column: name of column in pandas dataframe(s) used for the values
                of this series for the X Axis. This column will override the data
                column defined in the X Axis instance.
            formatting: formatting spec for value associated with Y Axis.
            name: series name (shown in legend and tooltip)
            styling: styling spec.
            entity: entity spec.
            show_in_legend: whether to show series in legend or not.
            required: Flag to make the Series mandatory. If required == True and no
                Data the widget will show an error. If required==False and no Data,
                the widget hides the Series.
            visible: Flag to make the Series visible when chart is loaded.
            point_label_column: name of column in dataframe(s) used for label of each
                point.
            tooltips: tooltip items to be displayed at Series level.
        """
        super().__init__(
            formatting=formatting,
            name=name,
            data_column=None,
            entity=entity,
            show_in_legend=show_in_legend,
            required=required,
            visible=visible,
            point_label_column=point_label_column,
            tooltips=tooltips,
            x_data_column=x_data_column,
        )
        self._low_column = low_data_column
        self._high_column = high_data_column

        self._styling = (
            AreaRangeSeriesStyling(color_spec=styling)
            if isinstance(styling, Palette)
            else styling
        )

    def validate(self, *, data: pd.DataFrame) -> None:
        """Validate if dataframe that will be used for series contains required columns.

        Args:
            data: pandas dataframe which will be used for table
            widget_id: id of table widget where this series is used
            path: path in storage linked to data

        """
        super().validate(data=data)

        super()._validate_data_column(
            data=data,
            data_column=self._low_column,
            data_column_name="low_column",
        )

        super()._validate_data_column(
            data=data,
            data_column=self._high_column,
            data_column_name="high_column",
        )

    def _build_extra_inputs(self) -> Dict[str, Any]:
        return {
            "lowValueKey": build_templated_strings(items=self._low_column),
            "highValueKey": build_templated_strings(items=self._high_column),
        }
