"""Specs for category axis of a Categorical chart."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links import WidgetField
from engineai.sdk.dashboard.links.abstract import AbstractFactoryLinkItemsHandler
from engineai.sdk.dashboard.links.typing import GenericLink
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.charts.band.band import AxisBand
from engineai.sdk.dashboard.widgets.components.charts.line.line import AxisLine

from ..exceptions import CategoricalValidateDataColumnNotFoundError


class CategoryAxis(AbstractFactoryLinkItemsHandler):
    """Specs for category axis of a Categorical chart."""

    @type_check
    def __init__(
        self,
        *,
        data_column: Union[str, GenericLink],
        label_column: Optional[Union[str, GenericLink]] = None,
        title: Union[str, GenericLink] = "",
        enable_crosshair: bool = False,
        line: Optional[AxisLine] = None,
        band: Optional[AxisBand] = None,
    ) -> None:
        """Construct category axis for a Categorical chart.

        Args:
            title: axis title.
            data_column: name of column in pandas
                dataframe(s) used for Category axis values.
            enable_crosshair: whether to enable crosshair that follows either
                the mouse pointer or the hovered point.
            label_column: name of column in pandas
                dataframe(s) used for the label of each category. Same values are
                used for each series.
            line: specs for chart axis line.
            band: specs for chart axis band.
        """
        super().__init__()
        self.__title = title
        self.__enable_crosshair = enable_crosshair

        self.__data_column = data_column
        self.__label_column = label_column or data_column
        self.__line = line
        self.__band = band

    @property
    def data_column(self) -> Union[str, GenericLink]:
        """Get Category  axis data column."""
        return self.__data_column

    def validate(self, data: pd.DataFrame, **kwargs: Any) -> None:
        """Validate Category Axis elements and Data.

        Args:
            data (pd.DataFrame): Data associated to the chart.

        """
        self._validate_data_column(
            widget_data=data,
            kwargs=kwargs,
            data_column=self.__data_column,
            data_column_name="data_column",
        )

        self._validate_data_column(
            widget_data=data,
            kwargs=kwargs,
            data_column=self.__label_column,
            data_column_name="label_column",
        )

    def _validate_data_column(
        self,
        *,
        widget_data: pd.DataFrame,
        kwargs: Any,
        data_column: Union[str, GenericLink],
        data_column_name: str,
    ) -> None:
        if isinstance(data_column, WidgetField):
            data_column.validate(
                data=widget_data,
                storage=kwargs["storage"],
                data_column_name=data_column_name,
            )
        elif isinstance(data_column, str) and data_column not in widget_data.columns:
            raise CategoricalValidateDataColumnNotFoundError(
                series_class_name=self.__class__.__name__,
                column_value=data_column,
                column_name=data_column_name,
            )

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "enableCrosshair": self.__enable_crosshair,
            "title": build_templated_strings(items=self.__title),
            "bands": [self.__band.build()] if self.__band is not None else [],
            "lines": [self.__line.build()] if self.__line is not None else [],
            "categories": {
                "idKey": build_templated_strings(items=self.__data_column),
                "labelKey": build_templated_strings(items=self.__label_column),
            },
        }
