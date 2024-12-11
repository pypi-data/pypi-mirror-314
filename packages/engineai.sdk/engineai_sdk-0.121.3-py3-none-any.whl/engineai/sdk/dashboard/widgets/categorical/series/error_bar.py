"""Spec for a Column Series of a Categorical widget."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links.typing import GenericLink
from engineai.sdk.dashboard.styling.color import Palette
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.charts.styling import (
    ErrorBarSeriesStyling,
)
from engineai.sdk.dashboard.widgets.components.charts.typing import TooltipItem

from .base import CategoricalBaseSeries


class ErrorBarSeries(CategoricalBaseSeries):
    """Spec forError Bar Series of a Categorical widget."""

    _INPUT_KEY = "errorBar"

    @type_check
    def __init__(
        self,
        *,
        low_data_column: Union[str, GenericLink],
        high_data_column: Union[str, GenericLink],
        name: Optional[Union[str, GenericLink]] = None,
        styling: Optional[Union[Palette, ErrorBarSeriesStyling]] = None,
        stack: Optional[Union[str, GenericLink]] = None,
        show_in_legend: bool = True,
        required: bool = True,
        visible: bool = True,
        tooltips: Optional[List[TooltipItem]] = None,
    ) -> None:
        """Construct Column Series.

        Args:
            low_data_column: name of column in pandas dataframe(s) used for the
                low value of this series.
            high_data_column: name of column in pandas dataframe(s) used for the high
                value of this series.
            name: series name (shown in legend and tooltip).
            styling: styling spec.
            stack: id of stack for column.
            show_in_legend: whether to show series in legend or not.
            required: Flag to make the Series mandatory. If required == True
                and no Data the widget will show an error. If required==False and no
                Data, the widget hides the Series.
            visible: Flag to make the Series visible when chart is loaded.
            tooltips: Tooltip items to show in the tooltip.
        """
        super().__init__(
            data_column=None,
            name=name,
            show_in_legend=show_in_legend,
            required=required,
            visible=visible,
            tooltips=tooltips,
        )
        self._styling = (
            ErrorBarSeriesStyling(color_spec=styling)
            if isinstance(styling, Palette)
            else styling
        )
        self._stack = stack  # not being used
        self._high_data_column = high_data_column
        self._low_data_column = low_data_column

    def _build_extra_inputs(self) -> Dict[str, Any]:
        return {
            "lowValueKey": build_templated_strings(items=self._low_data_column),
            "highValueKey": build_templated_strings(items=self._high_data_column),
        }

    def validate(self, data: pd.DataFrame, **kwargs: Any) -> None:
        """Validate Column Series elements and Data.

        Args:
            data: Data associated with the Series.
        """
        super().validate(data=data, **kwargs)

        super()._validate_data_column(
            widget_data=data,
            kwargs=kwargs,
            data_column=self._high_data_column,
            data_column_name="high_data_column",
        )

        super()._validate_data_column(
            widget_data=data,
            kwargs=kwargs,
            data_column=self._low_data_column,
            data_column_name="low_data_column",
        )

        if self._styling:
            self._styling.validate(data=data)
