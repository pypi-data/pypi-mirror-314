"""Spec fot Number Styling Dot."""

from typing import Optional

from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.styling.color.spec import ColorSpec
from engineai.sdk.dashboard.templated_string import TemplatedStringItem
from engineai.sdk.dashboard.widgets.components.items.styling.base import BaseItemStyling


class NumberStylingDot(BaseItemStyling):
    """Spec for Number Dot Styling class."""

    _INPUT_KEY: str = "dot"

    @type_check
    def __init__(
        self,
        *,
        color_spec: ColorSpec,
        data_column: Optional[TemplatedStringItem] = None,
    ) -> None:
        """Construct spec for Number Dot Styling.

        Args:
            color_spec (ColorSpec): specs for color.
            data_column (Optional[TemplatedStringItem]): styling value key.
        """
        super().__init__(
            color_spec=color_spec,
            data_column=data_column,
        )
