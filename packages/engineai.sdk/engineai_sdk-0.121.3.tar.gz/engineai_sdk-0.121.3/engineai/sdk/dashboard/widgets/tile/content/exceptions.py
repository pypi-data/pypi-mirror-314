"""Tile Widget Exceptions."""

from typing import Optional

from engineai.sdk.dashboard.widgets.tile.exceptions import TileWidgetError


class TileValidateValueError(TileWidgetError):
    """Tile Widget Validate Value Error."""

    def __init__(
        self,
        subclass: str,
        argument: str,
        value: str,
        widget_id: Optional[str] = None,
    ) -> None:
        """Tile Widget Validate Error constructor.

        Args:
            widget_id (str): Tile widget id.
            subclass (str): Tile Widget secondary class.
            argument (str): Tile widget argument.
            value (str): Tile widget value.
        """
        super().__init__(widget_id=widget_id)
        self.error_strings.append(
            f"Missing {argument}='{value}' in Data for the {subclass}."
        )
