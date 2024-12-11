"""Module that contains the Tile items validation failure handler."""

import warnings


class TileValidateValueWarning(Warning):
    """Tile Widget Validate Value Warning."""


def validation_failure_handler(
    required: bool,
    error: Exception,
) -> None:
    """Tile items validation failure handler.

    If the item is required, an error will be raised. Otherwise, only a warning will be
    show to user.

    Args:
        required: flag that indicated if the item is required.
        error (Exception): specs for the Tile Error that should be raised.
    """
    if required:
        raise error
    warning_type = TileValidateValueWarning
    warnings.warn(str(error), warning_type)
