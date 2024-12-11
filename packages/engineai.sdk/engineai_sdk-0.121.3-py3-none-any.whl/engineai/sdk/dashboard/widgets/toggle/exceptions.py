"""Toggle Widget Exceptions."""

from engineai.sdk.dashboard.exceptions import BaseDataValidationError


class ToggleValidateValueError(BaseDataValidationError):
    """Toggle Widget Validate Value Error."""

    def __init__(
        self,
        argument: str,
        value: str,
    ) -> None:
        """Toggle Widget Validate Error constructor.

        Args:
            argument (str): Toggle widget argument.
            value (str): Toggle widget value.
        """
        super().__init__(f"Missing {argument}='{value}' in Data.")
