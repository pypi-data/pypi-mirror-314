"""Serialization module."""

from .json import deserialize
from .json import serialize

default_serialize = serialize
default_deserialize = deserialize

__all__ = ["default_serialize", "default_deserialize"]
