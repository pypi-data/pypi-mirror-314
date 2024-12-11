"""Dashboard Data Module."""

from .decorator import DataSource
from .decorator import data_source
from .enums import StorageType

__all__ = ["data_source", "DataSource", "StorageType"]
