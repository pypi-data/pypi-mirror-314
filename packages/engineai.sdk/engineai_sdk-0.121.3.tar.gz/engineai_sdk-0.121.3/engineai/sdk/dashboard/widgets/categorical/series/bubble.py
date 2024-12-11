"""Spec for a Bubble Series of a Categorical widget."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting import NumberFormatting
from engineai.sdk.dashboard.links.typing import GenericLink
from engineai.sdk.dashboard.styling.color import Palette
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.charts.styling import (
    BubbleCircleSeriesStyling,
)
from engineai.sdk.dashboard.widgets.components.charts.styling import (
    BubbleCountrySeriesStyling,
)
from engineai.sdk.dashboard.widgets.components.charts.typing import TooltipItem

from .base import CategoricalBaseSeries

BubbleSeriesStyling = Union[BubbleCircleSeriesStyling, BubbleCountrySeriesStyling]


class BubbleSeries(CategoricalBaseSeries):
    """Spec for a Bubble Series of a Categorical widget."""

    _INPUT_KEY = "bubble"

    @type_check
    def __init__(
        self,
        *,
        bubble_size_data_column: Union[str, GenericLink],
        data_column: Union[str, GenericLink],
        name: Optional[Union[str, GenericLink]] = None,
        bubble_name: Optional[Union[str, GenericLink]] = None,
        bubble_size_formatting: Optional[NumberFormatting] = None,
        styling: Optional[Union[Palette, BubbleSeriesStyling]] = None,
        show_in_legend: bool = True,
        required: bool = True,
        visible: bool = True,
        tooltips: Optional[List[TooltipItem]] = None,
    ) -> None:
        """Construct a Bubble Series.

        Args:
            bubble_size_data_column: name of column in pandas dataframe(s) used for
                the values of this series associated with the size of the bubble.
            data_column: name of column in pandas dataframe(s) used for the values
                of this series for the Y Axis.
            name: series name (shown in legend and tooltip).
            bubble_name: name for the bubble value (show in tooltip).
            bubble_size_formatting: formatting spec for size of the bubble
                (used in tooltip).
            styling: styling spec.
            show_in_legend: whether to show series in legend or not.
            required: Flag to make the Series mandatory. If required == True
                and no Data the widget will show an error. If required==False and no
                Data, the widget hides the Series.
            visible: Flag to make the Series visible when chart is loaded.
            tooltips: Tooltip items to show in the tooltip.
        """
        super().__init__(
            data_column=data_column,
            name=name,
            show_in_legend=show_in_legend,
            required=required,
            visible=visible,
            tooltips=tooltips,
        )
        self._bubble_size_data_column = bubble_size_data_column
        self._bubble_name_column = self._set_name(
            name=bubble_name, data_column=bubble_size_data_column
        )

        self._bubble_size_formatting = (
            bubble_size_formatting if bubble_size_formatting else NumberFormatting()
        )
        self._styling = (
            BubbleCircleSeriesStyling(color_spec=styling)
            if isinstance(styling, Palette)
            else styling
        )

    def _build_extra_inputs(self) -> Dict[str, Any]:
        return {
            "zValueKey": build_templated_strings(items=self._bubble_size_data_column),
            "zValueTitle": build_templated_strings(items=self._bubble_name_column),
            "zValueFormatting": self._bubble_size_formatting.build(),
        }

    def validate(self, data: pd.DataFrame, **kwargs: Any) -> None:
        """Validate Bubble Series elements and Data.

        Args:
            data: Data associated with the Series.

        Raises:
            ValueError:
                - if bubble size column not found in Data columns.
        """
        super().validate(data=data, **kwargs)

        super()._validate_data_column(
            widget_data=data,
            kwargs=kwargs,
            data_column=self._bubble_size_data_column,
            data_column_name="bubble_size_data_column",
        )

        if self._styling:
            self._styling.validate(data=data)
