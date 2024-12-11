"""Spec for Pie Series."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

import pandas as pd

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting.number import NumberFormatting
from engineai.sdk.dashboard.styling.color import Palette
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.charts.typing import TooltipItems

from .base import BaseSeries
from .styling import SeriesStyling


class CountrySeries(BaseSeries):
    """Define country-based pie chart series.

    Define a series specifically for pie charts representing data
    categorized by country, with options for customizing country code
    column, data column, formatting, styling, and tooltips.
    """

    _INPUT_KEY = "country"

    @type_check
    def __init__(
        self,
        *,
        name: TemplatedStringItem = "Country Series",
        country_column: TemplatedStringItem = "country_code",
        data_column: TemplatedStringItem = "value",
        formatting: Optional[NumberFormatting] = None,
        styling: Optional[Union[Palette, SeriesStyling]] = None,
        tooltips: Optional[TooltipItems] = None,
    ) -> None:
        """Constructor for CountrySeries.

        Args:
            name: name for the Pie series.
            country_column: name of column in pandas dataframe(s) that has country code
                within the pie.
            data_column: name of column in pandas dataframe(s) that has pie data.
            formatting: spec for number formatting.
            styling: spec for pie series styling.
            tooltips: tooltip items to be displayed at Series level.

        Examples:
            ??? example "Create Pie Widget using a CountrySeries"
                ```py linenums="1"
                import pandas as pd
                from engineai.sdk.dashboard.dashboard import Dashboard
                from engineai.sdk.dashboard.widgets import pie
                data = pd.DataFrame(
                    {
                        "country": ["US", "FR"],
                        "volume": [10, 20],
                    },
                )
                dashboard = Dashboard(
                    content=pie.Pie(
                        data=data,
                        series=pie.CountrySeries(
                            country_column="name",
                            data_column="volume",
                        )
                    )
                )
                ```
        """
        super().__init__(
            name=name,
            category_column=country_column,
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
            field="country_column",
            item=self._category_column,
        )
        super().validate(data=data)

    def _build_category_key(self) -> Dict[str, Any]:
        return {
            "countryCodeKey": build_templated_strings(items=self._category_column),
        }
