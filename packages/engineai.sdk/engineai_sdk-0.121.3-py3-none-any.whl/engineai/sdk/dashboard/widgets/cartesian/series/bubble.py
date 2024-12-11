"""Spec for a bubble series of a Cartesian widget."""

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
    BubbleCircleSeriesStyling,
)
from engineai.sdk.dashboard.widgets.components.charts.styling import (
    BubbleCountrySeriesStyling,
)
from engineai.sdk.dashboard.widgets.components.charts.typing import TooltipItems

from .base import CartesianBaseSeries

BubbleSeriesStyling = Union[
    BubbleCircleSeriesStyling,
    BubbleCountrySeriesStyling,
]


class BubbleSeries(CartesianBaseSeries):
    """Spec for a bubble series of a Cartesian widget."""

    _INPUT_KEY = "bubble"
    _styling_class = BubbleCircleSeriesStyling

    @type_check
    def __init__(
        self,
        *,
        bubble_size_data_column: Union[str, GenericLink],
        data_column: Union[str, GenericLink],
        x_data_column: Optional[Union[str, GenericLink]] = None,
        formatting: Optional[NumberFormatting] = None,
        bubble_name: Optional[Union[str, GenericLink]] = None,
        name: Optional[Union[str, GenericLink]] = None,
        bubble_size_formatting: Optional[NumberFormatting] = None,
        styling: Optional[Union[Palette, BubbleSeriesStyling]] = None,
        entity: Optional[Entities] = None,
        show_in_legend: bool = True,
        required: bool = True,
        visible: bool = True,
        point_label_column: Optional[Union[str, GenericLink]] = None,
        tooltips: Optional[TooltipItems] = None,
    ) -> None:
        """Construct bubble series.

        Args:
            data_column: name of column in pandas dataframe(s) used for the values of
                this series for the Y Axis.
            x_data_column: name of column in pandas dataframe(s) used for the values
                of this series for the X Axis. This column will override the data
                column defined in the X Axis instance.
            formatting: formatting spec for value associated with Y Axis.
            name: series name (shown in legend and tooltip).
            bubble_name: name for the bubble value (show in tooltip).
            bubble_size_data_column: name of column in pandas dataframe(s) used for
                the values of this series associated with the size of the bubble.
            bubble_size_formatting: formatting spec for value associated with bubbles.
            styling: styling spec.
            entity: entity spec.
            show_in_legend: whether to show series in legend or not.
            required: Flag to make the Series mandatory. If required == True and no
                Data the widget will show an error. If required==False and no
                Data, the widget hides the Series.
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
            BubbleCircleSeriesStyling(color_spec=styling)
            if isinstance(styling, Palette)
            else styling
        )
        self._bubble_size_column = bubble_size_data_column
        self._bubble_name_column = self._set_name(
            name=bubble_name, data_column=bubble_size_data_column
        )

        self._bubble_size_formatting = (
            bubble_size_formatting if bubble_size_formatting else NumberFormatting()
        )

    def validate(self, *, data: pd.DataFrame) -> None:
        """Validate if dataframe that will be used for series contains required columns.

        Args:
            data: pandas dataframe which will be used for table
        """
        super().validate(data=data)

        super()._validate_data_column(
            data=data,
            data_column=self._bubble_size_column,
            data_column_name="bubble_size_column",
        )
        self._bubble_size_formatting.validate(data=data)

    def _build_extra_inputs(self) -> Dict[str, Any]:
        return {
            "zValueKey": (
                build_templated_strings(items=self._bubble_size_column)
                if self._bubble_size_column
                else {}
            ),
            "zValueTitle": (
                build_templated_strings(items=self._bubble_name_column)
                if self._bubble_name_column
                else {}
            ),
            "zValueFormatting": self._bubble_size_formatting.build(),
        }
