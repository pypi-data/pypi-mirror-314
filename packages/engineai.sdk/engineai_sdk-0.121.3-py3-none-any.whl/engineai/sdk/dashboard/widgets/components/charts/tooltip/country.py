"""Specs for country item for a tooltip."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from pandas import DataFrame

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.formatting.text import TextFormatting
from engineai.sdk.dashboard.links.abstract import AbstractFactoryLinkItemsHandler
from engineai.sdk.dashboard.templated_string import DataField
from engineai.sdk.dashboard.templated_string import InternalDataField
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.templated_string import build_templated_strings
from engineai.sdk.dashboard.widgets.components.charts.tooltip.exceptions import (
    TooltipItemColumnNotFoundError,
)

from .styling.country.typings import CountryTooltipItemStyling


class CountryTooltipItem(AbstractFactoryLinkItemsHandler):
    """Customize tooltips for numerical data in Chart.

    Define specifications for a Country item within a tooltip for a Chart
    widget to customize the appearance and content of tooltips displayed
    for country data.
    """

    @type_check
    def __init__(
        self,
        *,
        data_key: TemplatedStringItem,
        country: Union[str, DataField],
        styling: Optional[CountryTooltipItemStyling] = None,
        formatting: Optional[TextFormatting] = None,
    ) -> None:
        """Constructor for NumberTooltipItem.

        Args:
            data_key: name of key in pandas dataframe(s) used for the value of
                the tooltip item.
            country: country code.
            styling: styling specs.
            formatting: formatting specs.
        """
        super().__init__()
        self.__data_key = data_key
        self.__country = InternalDataField(country)
        self.__formatting = formatting or TextFormatting()
        self.__styling = styling

    @property
    def data_column(self) -> TemplatedStringItem:
        """Get data column."""
        return self.__data_key

    def validate(self, *, data: DataFrame) -> None:
        """Validate if dataframe that will be used for column contains required columns.

        Args:
            data (DataFrame): pandas dataframe which will be used for table
        """
        if isinstance(self.__data_key, str) and self.__data_key not in data.columns:
            raise TooltipItemColumnNotFoundError(
                class_name=self.__class__.__name__,
                column_name="data_column",
                column_value=self.__data_key,
            )
        self.__country.validate(data=data)

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "styling": self.__styling.build() if self.__styling else None,
            "country": self.__country.build(),
            "valueKey": build_templated_strings(items=self.__data_key),
            "formatting": self.__formatting.build(),
        }
