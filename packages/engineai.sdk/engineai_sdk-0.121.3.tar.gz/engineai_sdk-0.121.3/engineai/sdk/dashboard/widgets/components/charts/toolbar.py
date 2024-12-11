"""Specs for chart toolbar."""

from typing import Any
from typing import Dict


def build_chart_toolbar(enable: bool) -> Dict[str, Any]:
    """Build chart toolbar method."""
    return {"disabled": not enable}
