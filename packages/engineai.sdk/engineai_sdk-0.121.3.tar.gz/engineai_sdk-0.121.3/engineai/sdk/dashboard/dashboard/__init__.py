"""Spec for building a dashboard."""

from .dashboard import Dashboard
from .dashboard import PublishMode
from .dashboard import StorageType
from .page.page import Page
from .page.route import Route

__all__ = [
    # .dashboard
    "Dashboard",
    "PublishMode",
    "Page",
    "Route",
    "StorageType",
]
