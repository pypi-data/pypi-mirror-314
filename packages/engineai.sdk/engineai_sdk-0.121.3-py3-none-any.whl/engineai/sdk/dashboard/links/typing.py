"""Spec for Common Links spec used across the packages."""

from typing import Union

from .route_link import RouteLink
from .widget_field import WidgetField

GenericLink = Union[WidgetField, RouteLink]
