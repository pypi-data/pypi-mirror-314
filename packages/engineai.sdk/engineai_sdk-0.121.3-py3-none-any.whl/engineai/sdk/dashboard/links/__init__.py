"""Spec for Common Links spec used across the packages."""

from .route_link import RouteLink
from .url import UrlQueryDependency
from .web_component import WebComponentLink
from .widget_field import WidgetField

__all__ = [
    "WidgetField",
    "RouteLink",
    "UrlQueryDependency",
    "WebComponentLink",
]
