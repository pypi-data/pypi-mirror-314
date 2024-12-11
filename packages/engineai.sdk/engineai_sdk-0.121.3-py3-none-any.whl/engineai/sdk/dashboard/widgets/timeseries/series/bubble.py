"""Spec for a bubble series of a Timeseries widget."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting import NumberFormatting
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
    BubbleCircleSeriesStyling,
)
from engineai.sdk.dashboard.widgets.components.charts.styling import (
    BubbleCountrySeriesStyling,
)
from engineai.sdk.dashboard.widgets.components.charts.typing import TooltipItems
from engineai.sdk.dashboard.widgets.timeseries.transform import Transform

from .base import TimeseriesBaseSeries

BubbleSeriesStyling = Union[BubbleCircleSeriesStyling, BubbleCountrySeriesStyling]


class BubbleSeries(TimeseriesBaseSeries):
    """Visualize data with bubbles in Timeseries widget.

    Construct specifications for a bubble series within a Timeseries widget.
    Visually represent data with bubbles on the chart. The size of each
    bubble corresponds to a specific data value, providing an intuitive way
    to grasp the magnitude of each data point.
    """

    _INPUT_KEY = "bubble"
    _styling_class = BubbleCircleSeriesStyling

    @type_check
    def __init__(
        self,
        *,
        data_column: Union[str, WidgetField],
        bubble_size_data_column: Union[str, WidgetField],
        name: Optional[Union[str, GenericLink]] = None,
        bubble_name: Optional[Union[str, WidgetField]] = None,
        bubble_size_formatting: Optional[NumberFormatting] = None,
        styling: Optional[Union[Palette, BubbleSeriesStyling]] = None,
        entity: Optional[Entities] = None,
        show_in_legend: bool = True,
        required: bool = True,
        visible: bool = True,
        right_axis: bool = False,
        tooltips: Optional[TooltipItems] = None,
    ) -> None:
        """Constructor for BubbleSeries.

        Args:
            data_column: name of column in pandas dataframe(s) used for the values of
                this series associated with the y axis.
            bubble_size_data_column: name of column in pandas dataframe(s) used for
                the values of this series associated with the size of the bubble.
            name: series name (shown in legend and tooltip).
            bubble_name: name for the bubble value (show in tooltip).
            bubble_size_formatting: formatting spec for size of the bubble (used in
                tooltip).
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
                BubbleCircleSeriesStyling(color_spec=styling)
                if isinstance(styling, Palette)
                else styling
            ),
            entity=entity,
            right_axis=right_axis,
            tooltips=tooltips,
        )
        self._bubble_size_column: Union[str, WidgetField] = (
            bubble_size_data_column
            if isinstance(bubble_size_data_column, str)
            else bubble_size_data_column
        )
        self._bubble_name_column = self._set_name(
            name=bubble_name, data_column=bubble_size_data_column
        )

        self._bubble_size_formatting = (
            bubble_size_formatting if bubble_size_formatting else NumberFormatting()
        )
        self._bubble_transforms: List[Transform] = []

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

        if self._entity is not None and isinstance(self._entity, CountryEntity):
            self._entity.validate_data_column(data=data)

    def add_bubble_transform(self, *transform: Transform) -> "BubbleSeries":
        """Add transform (i.e. apply transform to series data with high column data).

        Returns:
            BubbleSeries: reference to this series to facilitate inline
                manipulation
        """
        self._bubble_transforms.extend(transform)
        return self

    def _build_extra_inputs(self) -> Dict[str, Any]:
        return {
            "zValueKey": build_templated_strings(items=self._bubble_size_column),
            "zValueName": build_templated_strings(items=self._bubble_name_column),
            "zValueFormatting": self._bubble_size_formatting.build(),
            "yTransforms": [transform.build() for transform in self._transforms],
            "zTransforms": [transform.build() for transform in self._bubble_transforms],
        }
