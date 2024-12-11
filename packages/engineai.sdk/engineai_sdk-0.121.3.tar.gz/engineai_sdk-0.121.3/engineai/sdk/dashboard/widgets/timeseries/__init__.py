"""Specs for Timeseries widget."""

from engineai.sdk.dashboard.widgets.components.charts.axis.label import AxisLabel
from engineai.sdk.dashboard.widgets.components.charts.axis.scale import AxisScaleDynamic
from engineai.sdk.dashboard.widgets.components.charts.axis.scale import (
    AxisScaleNegative,
)
from engineai.sdk.dashboard.widgets.components.charts.axis.scale import (
    AxisScalePositive,
)
from engineai.sdk.dashboard.widgets.components.charts.axis.scale import (
    AxisScaleSymmetric,
)
from engineai.sdk.dashboard.widgets.components.charts.band.band import AxisBand
from engineai.sdk.dashboard.widgets.components.charts.band.band import AxisBandStyling
from engineai.sdk.dashboard.widgets.components.charts.line.line import AxisLine
from engineai.sdk.dashboard.widgets.components.charts.line.line import AxisLineStyling
from engineai.sdk.dashboard.widgets.components.charts.series.entities.country import (
    CountryEntity,
)
from engineai.sdk.dashboard.widgets.components.charts.series.entities.custom import (
    CustomEntity,
)
from engineai.sdk.dashboard.widgets.components.charts.styling.enums import DashStyle
from engineai.sdk.dashboard.widgets.components.charts.styling.enums import MarkerSymbol
from engineai.sdk.dashboard.widgets.components.charts.typing import CategoryTooltipItem
from engineai.sdk.dashboard.widgets.components.charts.typing import DatetimeTooltipItem
from engineai.sdk.dashboard.widgets.components.charts.typing import NumberTooltipItem
from engineai.sdk.dashboard.widgets.components.charts.typing import TextTooltipItem

from .axis.x_axis import XAxis
from .axis.y_axis.y_axis import YAxis
from .axis.y_axis.y_axis_mirror import MirrorYAxis
from .chart import Chart
from .enums import TransformChoices
from .legend import LegendPosition
from .navigator import Navigator
from .period_selector.custom_period import CustomPeriod
from .period_selector.selector import PeriodSelector
from .period_selector.standard import Period
from .series.area import AreaSeries
from .series.area import AreaSeriesStyling
from .series.area_range import AreaRangeSeries
from .series.area_range import AreaRangeSeriesStyling
from .series.bubble import BubbleCircleSeriesStyling
from .series.bubble import BubbleCountrySeriesStyling
from .series.bubble import BubbleSeries
from .series.column import ColumnSeries
from .series.column import ColumnSeriesStyling
from .series.error_bar import ErrorBarSeries
from .series.error_bar import ErrorBarSeriesStyling
from .series.line import LineSeries
from .series.line import LineSeriesStyling
from .series.point import PointSeries
from .series.point import PointSeriesStyling
from .series.scatter import ScatterSeries
from .series.scatter import ScatterSeriesStyling
from .timeseries import Timeseries
from .transform import Transform

__all__ = [
    # .axis
    "XAxis",
    "YAxis",
    "MirrorYAxis",
    "AxisScaleSymmetric",
    "AxisScaleDynamic",
    "AxisScalePositive",
    "AxisScaleNegative",
    # ..charts
    "DashStyle",
    "MarkerSymbol",
    # .chart
    "Chart",
    # .period_selector
    "PeriodSelector",
    "CustomPeriod",
    "Period",
    # .series
    "LineSeries",
    "LineSeriesStyling",
    "AreaSeries",
    "AreaSeriesStyling",
    "AreaRangeSeries",
    "AreaRangeSeriesStyling",
    "BubbleSeries",
    "BubbleCircleSeriesStyling",
    "BubbleCountrySeriesStyling",
    "ColumnSeries",
    "ColumnSeriesStyling",
    "ScatterSeries",
    "ScatterSeriesStyling",
    "ErrorBarSeries",
    "ErrorBarSeriesStyling",
    "PointSeries",
    "PointSeriesStyling",
    # .legend
    "LegendPosition",
    # .navigator
    "Navigator",
    # .timeseries
    "Timeseries",
    # .tooltip
    "CategoryTooltipItem",
    "DatetimeTooltipItem",
    "NumberTooltipItem",
    "TextTooltipItem",
    # .transform
    "Transform",
    "TransformChoices",
    # .entities
    "CountryEntity",
    "CustomEntity",
    "AxisLine",
    "AxisBand",
    "AxisLabel",
    "AxisLineStyling",
    "AxisBandStyling",
]
