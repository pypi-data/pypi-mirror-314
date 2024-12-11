"""Specs for x axis of a Cartesian chart."""

from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import Mapping
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting import AxisNumberFormatting
from engineai.sdk.dashboard.links.abstract import AbstractFactoryLinkItemsHandler
from engineai.sdk.dashboard.links.typing import GenericLink
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.charts.axis.scale import AxisScale
from engineai.sdk.dashboard.widgets.components.charts.axis.scale import AxisScaleDynamic
from engineai.sdk.dashboard.widgets.components.charts.axis.scale import build_axis_scale


class CartesianBaseAxis(AbstractFactoryLinkItemsHandler):
    """Specs for X Axis of a Cartesian chart."""

    @type_check
    def __init__(
        self,
        *,
        title: Union[str, GenericLink] = "",
        enable_crosshair: bool = False,
        formatting: Optional[AxisNumberFormatting] = None,
        scale: Optional[AxisScale] = None,
    ) -> None:
        """Construct x axis for a Cartesian chart.

        Args:
            title: axis title.
            enable_crosshair: whether to enable crosshair that follows either
                the mouse pointer or the hovered point.
            formatting: formatting spec for axis labels.
            scale: y axis scale, one of AxisSymmetricScale, AxisDynamicScale,
                AxisPositiveScale, AxisNegativeScale.
        """
        super().__init__()
        self.__title = title

        self.__formatting = formatting or AxisNumberFormatting()

        self.__enable_crosshair = enable_crosshair
        self.__scale = scale or AxisScaleDynamic()

    def validate(
        self,
        *,
        data: pd.DataFrame,
    ) -> None:
        """Validate if dataframe has the required columns and dependencies for axis.

        Args:
            data: pandas dataframe which will be used for table.

        Raises:
            CartesianValidateSeriesDataColumnNotFound: when data is not found
        """
        self._axis_validate(data=data)
        self.__formatting.validate(data=data)

    @abstractmethod
    def _axis_validate(
        self,
        *,
        data: pd.DataFrame,
    ) -> None:
        """Validate Cartesian Axis."""

    def _build_extra_axis(self) -> Mapping[str, Any]:
        """Method that generates the input for axis extra attribute."""
        return {}

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API.
        """
        return {
            "enableCrosshair": self.__enable_crosshair,
            "title": build_templated_strings(items=self.__title),
            "scale": build_axis_scale(scale=self.__scale),
            "formatting": self.__formatting.build(),
            "bands": [],
            "lines": [],
            **self._build_extra_axis(),
        }
