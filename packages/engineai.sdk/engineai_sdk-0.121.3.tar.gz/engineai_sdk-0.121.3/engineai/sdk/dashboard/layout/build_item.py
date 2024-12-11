"""Spec to build different nested Grid items."""

from typing import Any
from typing import Dict


def build_item(item: Any) -> Dict[str, Any]:
    """Builds spec for dashboard API.

    Args:
        item (Any): item spec

    Returns:
        Input object for Dashboard API
    """
    return {item.input_key: item.build()}
