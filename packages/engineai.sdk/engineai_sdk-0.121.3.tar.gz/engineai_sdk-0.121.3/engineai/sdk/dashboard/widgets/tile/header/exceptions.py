"""Tile Widget Header Exceptions."""

from engineai.sdk.dashboard.widgets.tile.exceptions import TileWidgetError


class TileHeaderNoConfigurationError(TileWidgetError):
    """Tile Widget Header Validate No Data Error."""

    def __init__(
        self,
        *args: object,
    ) -> None:
        """Constructor for TileHeaderNoConfigurationError class.

        Args:
            widget_id (str): Tile widget id.
        """
        super().__init__(None, *args)
        self.error_strings.append(
            "All class variables are None. Please provide more information "
            "about the configuration."
        )
