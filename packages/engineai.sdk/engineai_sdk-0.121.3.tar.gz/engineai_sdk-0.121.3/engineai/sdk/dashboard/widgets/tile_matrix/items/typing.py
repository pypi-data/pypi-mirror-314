"""Typing for the tile matrix items."""

from typing import Union

from engineai.sdk.dashboard.widgets.components.actions.links import UrlLink
from engineai.sdk.dashboard.widgets.components.actions.links.external import (
    ExternalEvent,
)

Actions = Union[UrlLink, ExternalEvent]
