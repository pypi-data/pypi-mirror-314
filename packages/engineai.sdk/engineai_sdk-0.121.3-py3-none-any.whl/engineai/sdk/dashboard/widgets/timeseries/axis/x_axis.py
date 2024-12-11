"""Specs for x axis of a Timeseries chart."""

from typing import Any
from typing import Dict
from typing import Optional

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.links.abstract import AbstractFactoryLinkItemsHandler
from engineai.sdk.dashboard.widgets.components.charts.band.band import AxisBand
from engineai.sdk.dashboard.widgets.components.charts.line.line import AxisLine


class XAxis(AbstractFactoryLinkItemsHandler):
    """Specify x-axis appearance & behavior in Timeseries chart.

    Construct specifications for the x-axis of a Timeseries chart
    with a range of options to customize its appearance and behavior.
    """

    @type_check
    def __init__(
        self,
        *,
        enable_crosshair: bool = False,
        line: Optional[AxisLine] = None,
        band: Optional[AxisBand] = None,
    ) -> None:
        """Construct TimeseriesBaseAxis.

        Args:
            enable_crosshair: whether to enable crosshair that follows either
                the mouse pointer or the hovered point.
            line: line spec for y axis.
            band: band spec for y axis.
        """
        super().__init__()
        self.__enable_crosshair = enable_crosshair
        self.__line = line
        self.__band = band

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API.
        """
        return {
            "enableCrosshair": self.__enable_crosshair,
            "bands": [self.__band.build()] if self.__band is not None else [],
            "lines": [self.__line.build()] if self.__line is not None else [],
        }
