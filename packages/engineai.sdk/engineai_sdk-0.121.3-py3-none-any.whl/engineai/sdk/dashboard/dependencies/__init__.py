"""Specs for dependencies."""

from .datastore import DashboardBlobStorage
from .datastore import DashboardFileShareStorage
from .http import HttpDependency
from .route import RouteDependency
from .widget import WidgetSelectDependency

__all__ = [
    # .datastore
    "DashboardBlobStorage",
    "DashboardFileShareStorage",
    # .widget
    "WidgetSelectDependency",
    # .route
    "RouteDependency",
    # .http
    "HttpDependency",
]
