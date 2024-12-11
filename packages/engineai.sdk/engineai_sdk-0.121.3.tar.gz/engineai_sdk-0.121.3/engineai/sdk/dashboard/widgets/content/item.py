"""Spec for ContentItem class."""

from typing import Any
from typing import Dict
from typing import Union

from .markdown import MarkdownItem

ContentItem = Union[MarkdownItem]


def build_content_item(item: ContentItem) -> Dict[str, Any]:
    """Builds item for Content Widget.

    Args:
        item (ContentItem): Item to build.

    Returns:
        Input object for Dashboard API
    """
    if isinstance(item, MarkdownItem):
        return {"markdown": item.build()}
    msg = "Content `item` needs to be MarkdownItem."
    raise TypeError(msg)
