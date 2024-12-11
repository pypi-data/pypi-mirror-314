"""Spec for Pie Series Styling."""

from typing import Optional

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.styling.color.palette import Palette
from engineai.sdk.dashboard.styling.color.spec import ColorSpec
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.widgets.components.charts.styling.base import (
    BaseChartSeriesStyling,
)


class SeriesStyling(BaseChartSeriesStyling):
    """Style pie chart series.

    Specify styling options for pie chart series, including
    color specifications and data column mapping.
    """

    @type_check
    def __init__(
        self,
        color_spec: Optional[ColorSpec] = None,
        data_column: Optional[TemplatedStringItem] = None,
    ) -> None:
        """Constructor for SeriesStyling.

        Args:
            color_spec: specs for color.
            data_column: name of column in pandas dataframe(s)
                that has the styling value.

        Examples:
            ??? example "Change color of Pie Widget series"
                ```py linenums="1"
                import pandas as pd
                from engineai.sdk.dashboard.dashboard import Dashboard
                from engineai.sdk.dashboard.styling import color
                from engineai.sdk.dashboard.widgets import pie
                data = pd.DataFrame(
                    {
                        "category": ["A", "B"],
                        "value": [1, 2],
                    },
                )
                dashboard = Dashboard(
                    content=pie.Pie(
                        data=data,
                        series=pie.Series(
                            styling = pie.SeriesStyling(
                                color_spec=color.Palette.BANANA_YELLOW,
                            )
                        ),
                    )
                )
                ```

            ??? example "Coloring Pie Widget segments using a discrete color mapping"
                ```py linenums="11"
                dashboard = Dashboard(
                    content=pie.Pie(
                        data=data,
                        series=pie.Series(
                            styling=pie.SeriesStyling(
                                color_spec=color.DiscreteMap(
                                    color.DiscreteMapValueItem(
                                        value=1,
                                        color=color.Palette.BANANA_YELLOW,
                                    ),
                                    color.DiscreteMapValueItem(
                                        value=2,
                                        color=color.Palette.RUBI_RED,
                                    ),
                                ),
                                data_column="value",
                            )
                        ),
                    )
                )
                ```
        """
        if color_spec is None:
            color_spec = Palette.MINT_GREEN
        super().__init__(data_column=data_column, color_spec=color_spec)
