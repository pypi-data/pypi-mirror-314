"""Spec for a Scatter Series of a Categorical widget."""

from typing import Any
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links.typing import GenericLink
from engineai.sdk.dashboard.styling.color import Palette
from engineai.sdk.dashboard.widgets.components.charts.styling import (
    ScatterSeriesStyling,
)
from engineai.sdk.dashboard.widgets.components.charts.typing import TooltipItem

from .base import CategoricalBaseSeries


class ScatterSeries(CategoricalBaseSeries):
    """Spec for a Scatter Series of a Categorical widget."""

    _INPUT_KEY = "scatter"

    @type_check
    def __init__(
        self,
        *,
        data_column: Union[str, GenericLink],
        name: Optional[Union[str, GenericLink]] = None,
        styling: Optional[Union[Palette, ScatterSeriesStyling]] = None,
        show_in_legend: bool = True,
        required: bool = True,
        visible: bool = True,
        tooltips: Optional[List[TooltipItem]] = None,
    ) -> None:
        """Construct Scatter Series.

        Args:
            data_column: name of column in pandas dataframe(s) used for the values
                of this series for the Y Axis.
            name: series name (shown in legend and tooltip).
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
        self._styling = (
            ScatterSeriesStyling(color_spec=styling)
            if isinstance(styling, Palette)
            else styling
        )

    def validate(self, data: pd.DataFrame, **kwargs: Any) -> None:
        """Validate Scatter Series elements and Data.

        Args:
            data: Data associated with the Series.
        """
        super().validate(data=data, **kwargs)
        if self._styling:
            self._styling.validate(data=data)
