"""Typing for the dashboard SDK."""

from typing import Any
from typing import Dict
from typing import TypedDict

from typing_extensions import NotRequired

from engineai.sdk.dashboard.clients.storage import StorageConfig

from .selectable_widgets import AbstractSelectWidget


class PrepareParams(TypedDict):
    """Parameters for kwargs in prepare method."""

    # General
    dashboard_slug: str
    storage_type: NotRequired[Any]
    page: NotRequired[Any]
    storage: NotRequired[StorageConfig]
    selectable_widgets: NotRequired[Dict[str, AbstractSelectWidget]]
