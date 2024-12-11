"""Specs for x axis of a Cartesian chart."""

from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting import AxisNumberFormatting
from engineai.sdk.dashboard.links.typing import GenericLink
from engineai.sdk.dashboard.widgets.cartesian.exceptions import (
    CartesianValidateDataColumnNotFoundError,
)
from engineai.sdk.dashboard.widgets.components.charts.axis.scale import AxisScale

from .base import CartesianBaseAxis


class XAxis(CartesianBaseAxis):
    """Specs for X Axis of a Cartesian chart."""

    @type_check
    def __init__(
        self,
        data_column: Union[str, GenericLink],
        *,
        title: Union[str, GenericLink] = "X",
        enable_crosshair: bool = False,
        formatting: Optional[AxisNumberFormatting] = None,
        scale: Optional[AxisScale] = None,
    ) -> None:
        """Construct x axis for a Cartesian chart.

        Args:
            data_column: name of column in pandas
                dataframe(s) used for X axis values.
            title: axis title
            enable_crosshair: whether to enable crosshair that follows either
                the mouse pointer or the hovered point.
            formatting: formatting spec for axis labels.
            scale: X axis scale.
        """
        super().__init__(
            title=title,
            enable_crosshair=enable_crosshair,
            formatting=formatting,
            scale=scale,
        )

        self.__data_column = data_column

    @property
    def data_column(self) -> Union[str, GenericLink]:
        """Get X axis data column."""
        return self.__data_column

    def _axis_validate(self, *, data: pd.DataFrame) -> None:
        if isinstance(self.data_column, str) and self.data_column not in data.columns:
            raise CartesianValidateDataColumnNotFoundError(
                class_name=self.__class__.__name__,
                column_name="data_column",
                column_value=self.data_column,
            )
