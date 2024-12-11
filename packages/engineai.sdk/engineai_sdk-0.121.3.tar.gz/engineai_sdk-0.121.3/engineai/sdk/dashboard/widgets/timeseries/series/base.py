"""Spec for a area series of a Timeseries widget."""

import re
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links.typing import GenericLink
from engineai.sdk.dashboard.styling.color.palette import qualitative_palette
from engineai.sdk.dashboard.styling.color.typing import ColorSpec
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.charts.series.base import ChartSeriesBase
from engineai.sdk.dashboard.widgets.components.charts.series.entities.custom import (
    CustomEntity,
)
from engineai.sdk.dashboard.widgets.components.charts.series.entities.typing import (
    Entities,
)
from engineai.sdk.dashboard.widgets.components.charts.styling.typing import (
    ColoredSeriesStyling,
)
from engineai.sdk.dashboard.widgets.components.charts.styling.typing import (
    SeriesStyling,
)
from engineai.sdk.dashboard.widgets.components.charts.tooltip.item import (
    build_tooltip_item,
)
from engineai.sdk.dashboard.widgets.components.charts.typing import TooltipItems
from engineai.sdk.dashboard.widgets.timeseries.exceptions import (
    TimeseriesValidateSeriesDataColumnNotFoundError,
)
from engineai.sdk.dashboard.widgets.timeseries.transform import Transform
from engineai.sdk.dashboard.widgets.utils import get_tooltips


class TimeseriesBaseSeries(ChartSeriesBase):
    """Spec for a Base Series of a Timeseries widget."""

    _styling_class: Optional[Type[ColoredSeriesStyling]] = None
    _INPUT_KEY: Optional[str] = None

    @type_check
    def __init__(
        self,
        *,
        name: Optional[Union[str, GenericLink]] = None,
        data_column: Optional[Union[str, GenericLink]],
        styling: Optional[SeriesStyling] = None,
        entity: Optional[Entities] = None,
        show_in_legend: bool = True,
        required: bool = True,
        visible: bool = True,
        right_axis: bool = False,
        tooltips: Optional[TooltipItems] = None,
    ) -> None:
        """Construct area series.

        Args:
            name: series name (shown in legend and tooltip).
            data_column: name of column in pandas dataframe(s) used for the values of
                this series.
            styling: styling spec.
                Defaults to None, i.e. picks color automatically from palette.
            entity: entity spec.
            show_in_legend: whether to show series in legend or not.
            required: Flag to make the Series mandatory. If required == True and no
                Data the widget will show an error. If required==False and no Data,
                the widget hides the Series.
            visible: Flag to make the Series visible when chart is loaded.
            right_axis: Flag to make the Series visible on the right axis. Only works
                when used in set_series, otherwise ignored.
            tooltips: tooltip items to be displayed at Series level.
        """
        super().__init__(name=name, data_column=data_column)
        self._data_column = data_column
        self._show_in_legend = show_in_legend
        self._tooltip_items = get_tooltips(tooltips)
        self._required = required
        self._visible = visible
        self._styling = styling
        self._entity = entity or CustomEntity(self.name)
        self._transforms: List[Transform] = []
        self._date_column: TemplatedStringItem = " "
        self.__is_right_axis = right_axis

    @property
    def is_right_axis(self) -> bool:
        """Flag to make the Series visible on the right axis."""
        return self.__is_right_axis

    @property
    def _input_key(self) -> str:
        """Returns styling Input Key argument value."""
        if self._INPUT_KEY is None:
            msg = f"Class {self.__class__.__name__}._INPUT_KEY not defined."
            raise NotImplementedError(msg)
        return self._INPUT_KEY

    def add_transforms(self, *transform: Transform) -> "TimeseriesBaseSeries":
        """Add transform (i.e. apply transform to series data with low column data).

        Returns:
            AreaSeries: reference to this series to facilitate inline
                manipulation
        """
        self._transforms.extend(transform)
        return self

    def prepare(self, date_column: TemplatedStringItem, index: int) -> None:
        """Prepare series to be rendered."""
        self._date_column = date_column
        if self._styling is None:
            self.__set_default_styling(color=qualitative_palette(index=index))
        else:
            self._styling.prepare(self._data_column)

    def validate(self, *, data: pd.DataFrame) -> None:
        """Validate if dataframe that will be used for series contains required columns.

        Args:
            data: pandas dataframe which will be used for table
        """
        self._validate_data_column(
            data=data, data_column=self._data_column, data_column_name="data_column"
        )

        for item in self._tooltip_items:
            item.validate(data=data)

        if self._styling is not None:
            self._styling.validate(data=data)

    def build(self) -> Dict[str, Any]:
        """Build series Input spec."""
        return {self._input_key: self._build_series()}

    def _validate_data_column(
        self,
        *,
        data: pd.DataFrame,
        data_column: Optional[Union[str, GenericLink]],
        data_column_name: str,
    ) -> None:
        if (
            data_column is not None
            and isinstance(data_column, str)
            and not re.search("{{(.*?)}}", data_column)
            and data_column not in data.columns
        ):
            # TODO: find a way to validate templated strings
            raise TimeseriesValidateSeriesDataColumnNotFoundError(
                series_class_name=self.__class__.__name__,
                column_name=data_column_name,
                column_value=data_column,
            )

    def _build_series(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "name": build_templated_strings(items=self.name),
            "xAxisKey": build_templated_strings(items=self._date_column),
            "showInLegend": self._show_in_legend,
            "tooltipItems": [
                build_tooltip_item(item=item) for item in self._tooltip_items
            ],
            "required": self._required,
            "isVisible": self._visible,
            "styling": self._styling.build() if self._styling is not None else None,
            "entity": self._entity.build(),
            **self._build_extra_inputs(),
            **self._build_y_axis_key(),
        }

    def _build_y_axis_key(self) -> Dict[str, Any]:
        return (
            {"yAxisKey": build_templated_strings(items=self._data_column)}
            if self._data_column is not None
            else {}
        )

    def _build_extra_inputs(self) -> Dict[str, Any]:
        return {}

    def __set_default_styling(self, color: ColorSpec) -> None:
        if self._styling_class is None:
            msg = (
                f"Class {self.__class__.__name__} does not have the variable "
                f"`_styling_class` initialized."
            )
            raise NotImplementedError(msg)
        self._styling = self.__create_styling(self._styling_class, color=color)

    def __create_styling(
        self, styling_class: Type[ColoredSeriesStyling], color: ColorSpec
    ) -> ColoredSeriesStyling:
        return styling_class(color_spec=color)
