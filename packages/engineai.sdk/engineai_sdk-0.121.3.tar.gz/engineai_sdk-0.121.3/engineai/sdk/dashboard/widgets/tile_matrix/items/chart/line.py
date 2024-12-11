"""Spec for Tile Matrix Widget Line Chart Item."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting.number import NumberFormatting
from engineai.sdk.dashboard.styling.color.palette import Palette
from engineai.sdk.dashboard.templated_string import DataField
from engineai.sdk.dashboard.templated_string import InternalDataField
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.widgets.components.items.styling import LineChartItemStyling

from ..typing import Actions
from .base import BaseTileMatrixChartItem


class LineChartItem(BaseTileMatrixChartItem):
    """Spec for Tile Matrix Line Chart Item."""

    _API_CHART_TYPE = "line"

    @type_check
    def __init__(
        self,
        *,
        data_column: TemplatedStringItem,
        label: Optional[Union[TemplatedStringItem, DataField]] = None,
        icon: Optional[Union[TemplatedStringItem, DataField]] = None,
        link: Optional[Actions] = None,
        formatting: Optional[NumberFormatting] = None,
        styling: Optional[Union[Palette, LineChartItemStyling]] = None,
        reference_line: Optional[Union[int, float, DataField]] = None,
    ) -> None:
        """Construct spec for the TileMatrixLineChartItem class.

        Args:
            data_column: column that has the value to be represented.
            label: Label text to be displayed.
            icon: icon to be displayed.
            link: link or action to be executed in the URL Icon.
            formatting: formatting spec.
            styling: styling spec.
            reference_line: spec for a fixed reference line.
        """
        super().__init__(
            data_column=data_column,
            label=label,
            icon=icon,
            link=link,
            formatting=formatting or NumberFormatting(),
            styling=(
                LineChartItemStyling(color_spec=styling)
                if isinstance(styling, Palette)
                else LineChartItemStyling()
                if styling is None
                else styling
            ),
        )

        self.__set_reference_line(reference_line)

    def __set_reference_line(
        self, reference_line: Optional[Union[int, float, DataField]]
    ) -> None:
        if reference_line is None:
            self.__reference_line = None
        elif isinstance(reference_line, (DataField)):
            self.__reference_line = InternalDataField(reference_line)
        else:
            self.__reference_line = InternalDataField(str(reference_line))

    def _build_extra_chart_inputs(self) -> Dict[str, Any]:
        """Build extra inputs for the chart."""
        if self.__reference_line:
            return {"referenceLine": self.__reference_line.build()}
        return {}
