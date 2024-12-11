"""Spec for a Area Series of a Categorical widget."""

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
from engineai.sdk.dashboard.widgets.components.charts.styling.area import (
    AreaSeriesStyling,
)
from engineai.sdk.dashboard.widgets.components.charts.typing import TooltipItem

from .base import CategoricalBaseSeries


class AreaSeries(CategoricalBaseSeries):
    """Spec for a Area Series of a Categorical widget."""

    _INPUT_KEY = "area"

    @type_check
    def __init__(
        self,
        *,
        data_column: Union[str, GenericLink],
        name: Optional[Union[str, GenericLink]] = None,
        styling: Optional[Union[Palette, AreaSeriesStyling]] = None,
        stacked: bool = False,
        show_in_legend: bool = True,
        required: bool = True,
        visible: bool = True,
        tooltips: Optional[List[TooltipItem]] = None,
    ) -> None:
        """Construct Area Series.

        Args:
            data_column: name of column in pandas dataframe(s) used for the values
                of this series for the Y Axis.
            name: series name (shown in legend and tooltip).
            styling: styling spec.
            stacked: whether area is stacked or not.
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
        self._stacked = stacked
        self._styling = (
            AreaSeriesStyling(color_spec=styling)
            if isinstance(styling, Palette)
            else styling
        )

    def _build_extra_inputs(self) -> Dict[str, Any]:
        return {
            "stack": build_templated_strings(
                items="stack" if self._stacked else self.name
            )
        }

    def validate(self, data: pd.DataFrame, **kwargs: Any) -> None:
        """Validate Area Series elements and Data.

        Args:
            data: Data associated with the Series.
        """
        super().validate(data=data, **kwargs)
        if self._styling:
            self._styling.validate(data=data)
