"""Platform SDK package."""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version

try:
    __version__ = version(__package__)
except PackageNotFoundError:
    __version__ = version(__package__.replace(".", "-"))
