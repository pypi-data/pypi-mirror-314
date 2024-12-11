"""Spec for a scatter series of a Cartesian widget."""

from typing import Optional
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting import NumberFormatting
from engineai.sdk.dashboard.links.typing import GenericLink
from engineai.sdk.dashboard.styling.color import Palette
from engineai.sdk.dashboard.widgets.components.charts.series.entities.typing import (
    Entities,
)
from engineai.sdk.dashboard.widgets.components.charts.styling import (
    ScatterSeriesStyling,
)
from engineai.sdk.dashboard.widgets.components.charts.typing import TooltipItems

from .base import CartesianBaseSeries


class ScatterSeries(CartesianBaseSeries):
    """Spec for a scatter series of a Cartesian widget."""

    _INPUT_KEY = "scatter"
    _styling_class = ScatterSeriesStyling

    @type_check
    def __init__(
        self,
        *,
        data_column: Union[str, GenericLink],
        x_data_column: Optional[Union[str, GenericLink]] = None,
        formatting: Optional[NumberFormatting] = None,
        name: Optional[Union[str, GenericLink]] = None,
        entity: Optional[Entities] = None,
        styling: Optional[Union[Palette, ScatterSeriesStyling]] = None,
        show_in_legend: bool = True,
        required: bool = True,
        visible: bool = True,
        point_label_column: Optional[Union[str, GenericLink]] = None,
        tooltips: Optional[TooltipItems] = None,
    ) -> None:
        """Construct scatter series.

        Args:
            data_column: name of column in pandas dataframe(s) used for the values of
                this series for the Y Axis.
            x_data_column: name of column in pandas dataframe(s) used for the values
                of this series for the X Axis. This column will override the data
                column defined in the X Axis instance.
            formatting: formatting spec for value associated with Y Axis.
            name: series name (shown in legend and tooltip).
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
            data_column=data_column,
            formatting=formatting,
            name=name,
            entity=entity,
            show_in_legend=show_in_legend,
            required=required,
            visible=visible,
            point_label_column=point_label_column,
            tooltips=tooltips,
            x_data_column=x_data_column,
        )
        self._styling = (
            ScatterSeriesStyling(color_spec=styling)
            if isinstance(styling, Palette)
            else styling
        )
