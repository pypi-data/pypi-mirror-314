"""Typing for entities."""

from typing import Union

from engineai.sdk.dashboard.widgets.components.charts.series.entities.country import (
    CountryEntity,
)
from engineai.sdk.dashboard.widgets.components.charts.series.entities.custom import (
    CustomEntity,
)

Entities = Union[CountryEntity, CustomEntity]
