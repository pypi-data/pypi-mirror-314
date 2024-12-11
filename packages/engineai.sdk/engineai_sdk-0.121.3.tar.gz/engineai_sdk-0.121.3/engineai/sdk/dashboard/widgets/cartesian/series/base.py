"""Spec for the CartesianBaseSeries widget."""

import warnings
from typing import Any
from typing import Dict
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting import NumberFormatting
from engineai.sdk.dashboard.links.typing import GenericLink
from engineai.sdk.dashboard.styling.color.palette import qualitative_palette
from engineai.sdk.dashboard.styling.color.typing import ColorSpec
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.cartesian.exceptions import (
    CartesianValidateDataColumnNotFoundError,
)
from engineai.sdk.dashboard.widgets.components.charts.series.base import ChartSeriesBase
from engineai.sdk.dashboard.widgets.components.charts.series.entities.country import (
    CountryEntity,
)
from engineai.sdk.dashboard.widgets.components.charts.series.entities.custom import (
    CustomEntity,
)
from engineai.sdk.dashboard.widgets.components.charts.series.entities.typing import (
    Entities,
)
from engineai.sdk.dashboard.widgets.components.charts.styling.typing import (
    ColoredSeriesStyling,
)
from engineai.sdk.dashboard.widgets.components.charts.tooltip.item import (
    build_tooltip_item,
)
from engineai.sdk.dashboard.widgets.components.charts.typing import TooltipItems
from engineai.sdk.dashboard.widgets.utils import get_tooltips

CartesianSeriesT = TypeVar(  # pylint: disable=typevar-name-incorrect-variance
    "CartesianSeriesT", bound="CartesianBaseSeries", covariant=True
)


class CartesianBaseSeries(ChartSeriesBase):
    """Spec for the CartesianBaseSeries widget."""

    _styling_class: Optional[Type[ColoredSeriesStyling]] = None
    _INPUT_KEY: Optional[str] = None

    @type_check
    def __init__(
        self,
        *,
        data_column: Optional[Union[str, GenericLink]] = None,
        x_data_column: Optional[Union[str, GenericLink]] = None,
        formatting: Optional[NumberFormatting] = None,
        name: Optional[Union[str, GenericLink]] = None,
        entity: Optional[Entities] = None,
        show_in_legend: bool = True,
        required: bool = True,
        visible: bool = True,
        point_label_column: Optional[Union[str, GenericLink]] = None,
        tooltips: Optional[TooltipItems] = None,
    ) -> None:
        """Spec for the CartesianBaseSeries widget.

        Args:
            data_column: name of column in pandas dataframe(s) used for the values
                of this series for the Y Axis.
            x_data_column: name of column in pandas dataframe(s) used for the values
                of this series for the X Axis. This column will override the data
                column defined in the X Axis instance.
            formatting: formatting spec for value associated with Y Axis.
            name: series name (shown in legend and tooltip).
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
        super().__init__(name=name, data_column=data_column)
        self._formatting = formatting or NumberFormatting()
        self._data_column = data_column
        self._show_in_legend = show_in_legend
        self._tooltip_items = get_tooltips(tooltips)
        self._index = 0
        self._required = required
        self._visible = visible
        self._styling: Optional[Any] = None
        self._x_column: TemplatedStringItem = x_data_column
        self._entity = entity or CustomEntity(self.name)

        if point_label_column is None:
            warnings.warn(
                "Missing point_label_column. Series name will be used as "
                "top label in tooltip"
            )
        self._point_label_column = point_label_column

    @property
    def _input_key(self) -> str:
        """Returns styling Input Key argument value."""
        if self._INPUT_KEY is None:
            msg = f"Class {self.__class__.__name__}._INPUT_KEY not defined."
            raise NotImplementedError(msg)
        return self._INPUT_KEY

    def validate(self, *, data: pd.DataFrame) -> None:
        """Validate if dataframe that will be used for series contains required columns.

        Args:
            data: pandas dataframe which will be used for table
        """
        self._validate_data_column(
            data=data,
            data_column=self._data_column,
            data_column_name="data_column",
        )

        self._validate_data_column(
            data=data,
            data_column=self._x_column,
            data_column_name="x_column",
        )

        for item in self._tooltip_items:
            item.validate(data=data)

        if self._styling is not None:
            self._styling.validate(data=data)

        if self._entity is not None and isinstance(self._entity, CountryEntity):
            self._entity.validate_data_column(data=data)

    def prepare(self, x_column: TemplatedStringItem, index: int) -> None:
        """Prepare series to be rendered."""
        self._x_column = self._x_column or x_column
        if self._styling is None:
            self.__set_default_styling(color=qualitative_palette(index=index))
        else:
            self._styling.prepare(self._data_column)

    def build(self) -> Dict[str, Any]:
        """Build Input spec for Dashboard API."""
        return {
            self._input_key: self._build_series(),
        }

    def _build_extra_inputs(self) -> Dict[str, Any]:
        return {}

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
            # Make sure that the column
            # is not a link composed with a string
            and "." not in data_column
            and data_column not in data.columns
        ):
            raise CartesianValidateDataColumnNotFoundError(
                class_name=self.__class__.__name__,
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
            "xAxisKey": build_templated_strings(items=self._x_column),
            "showInLegend": self._show_in_legend,
            "required": self._required,
            "isVisible": self._visible,
            "tooltipItems": [
                build_tooltip_item(item=item) for item in self._tooltip_items
            ],
            "styling": self._styling.build() if self._styling else None,
            "pointLabelKey": (
                build_templated_strings(items=self._point_label_column)
                if self._point_label_column
                else None
            ),
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
