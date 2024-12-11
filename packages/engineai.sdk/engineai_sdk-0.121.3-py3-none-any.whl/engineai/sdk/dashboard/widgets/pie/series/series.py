"""Spec for Pie Series."""

from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting.number import NumberFormatting
from engineai.sdk.dashboard.styling.color import Palette
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.widgets.components.charts.typing import TooltipItems

from .base import BaseSeries
from .styling import SeriesStyling


class Series(BaseSeries):
    """Define pie chart series.

    Define a generic series for the pie chart, specifying
    category and data columns, formatting, styling, and tooltips.
    """

    _INPUT_KEY = "standard"

    @type_check
    def __init__(
        self,
        *,
        name: TemplatedStringItem = "Series",
        category_column: TemplatedStringItem = "category",
        data_column: TemplatedStringItem = "value",
        formatting: Optional[NumberFormatting] = None,
        styling: Optional[Union[Palette, SeriesStyling]] = None,
        tooltips: Optional[TooltipItems] = None,
    ) -> None:
        """Constructor for Series.

        Args:
            name: name for the Pie series.
            category_column: name of column in pandas dataframe(s) that has category
                info within the pie.
            data_column: name of column in pandas dataframe(s) that has pie data.
            formatting: spec for number formatting.
            styling: spec for pie series styling.
            tooltips: tooltip items to be displayed at Series level.

        Examples:
            ??? example "Customise Pie Widget series (e.g. changing data column)"
                ```py linenums="1"
                import pandas as pd
                from engineai.sdk.dashboard.dashboard import Dashboard
                from engineai.sdk.dashboard.widgets import pie
                data = pd.DataFrame(
                    {
                        "name": ["X", "Y"],
                        "volume": [10, 20],
                    },
                )
                dashboard = Dashboard(
                    content=pie.Pie(
                        data=data,
                        series=pie.Series(
                            category_column="name",
                            data_column="volume",
                        )
                    )
                )
                ```
        """
        super().__init__(
            name=name,
            category_column=category_column,
            data_column=data_column,
            formatting=formatting,
            styling=styling,
            tooltips=tooltips,
        )

    def validate(
        self,
        *,
        data: pd.DataFrame,
    ) -> None:
        """Validates Pie Series Widget and the inner components specs."""
        self._validate_field(
            data=data,
            field="category_column",
            item=self._category_column,
        )
        super().validate(data=data)
