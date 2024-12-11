"""Dashboard Widget Exception."""

from typing import Optional

from engineai.sdk.dashboard.exceptions import DashboardError
from engineai.sdk.dashboard.exceptions import EngineAIDashboardError
from engineai.sdk.dashboard.utils import is_uuid


class DashboardWidgetError(EngineAIDashboardError):
    """Dashboard Widget Exception."""

    CLASS_NAME: Optional[str] = None

    def __init__(self, widget_id: Optional[str], *args: object) -> None:
        """Constructor for Dashboard Widget Exception.

        Args:
            widget_id (Optional[str]): id for widget.
        """
        super().__init__(widget_id, *args)
        if widget_id is not None and not is_uuid(widget_id):
            message = f"{self._class_name} widget with {widget_id=}."
        elif widget_id is not None and is_uuid(widget_id):
            message = (
                f"{self._class_name} widget error (to track which widget raised "
                "an error set the widget_id "
                f"example {self._class_name}(widget_id='example_id'))."
            )
        else:
            message = f"{self._class_name} widget error."

        self.error_strings.append(message)

    @property
    def _class_name(self) -> str:
        if self.CLASS_NAME is None:
            msg = "Variable CLASS_NAME not implemented."
            raise NotImplementedError(msg)
        return self.CLASS_NAME


class WidgetIdValueError(DashboardWidgetError):
    """Widget has a wrong widget_id."""

    def __init__(self, class_name: str, widget_id: str, *args: object) -> None:
        """Constructor for WidgetNoIndirectDependenciesError class.

        Args:
            class_name (str): widget type.
            widget_id (str): table widget id.
        """
        self.CLASS_NAME = class_name
        super().__init__(widget_id, class_name, *args)
        self.error_strings.append(
            "Must be alphanumerical and can include underscores and dashes."
        )


class WidgetTemplateStringWidgetNotFoundError(DashboardError):
    """Widget Template String Widget Not Found."""

    def __init__(
        self, slug: str, widget_id: str, template_widget_id: str, *args: object
    ) -> None:
        """Constructor for WidgetTemplateStringWidgetNotFoundError class."""
        super().__init__(slug, widget_id, template_widget_id, *args)
        self.error_strings.append(
            f"Select widget with widget_id='{template_widget_id}' used as template "
            f"string in Widget with {widget_id=} not found in Layout."
        )


class WidgetMinimumHeightError(DashboardWidgetError):
    """Widget minimum height error."""

    def __init__(self, widget_id: str, class_name: str, *args: object) -> None:
        """Constructor for WidgetMinimumHeightError class.

        Args:
            widget_id (str): widget id
            class_name (str): widget type.
        """
        super().__init__(widget_id, class_name, *args)
        self.CLASS_NAME = class_name
        self.error_strings.append("Argument `height` must be greater than 0.")


class WidgetInvalidHeightError(DashboardWidgetError):
    """Widget invalid height error."""

    def __init__(
        self, widget_id: str, class_name: str, steps: float, *args: object
    ) -> None:
        """Constructor for WidgetInvalidHeightError class.

        Args:
            widget_id (str): widget id
            class_name (str): widget type.
            steps (float): widget height step
        """
        super().__init__(widget_id, class_name, steps, *args)
        self.CLASS_NAME = class_name
        examples = [str(1 + n * steps) for n in range(4)]
        self.error_strings.append(
            f"Argument `height` must have a step increments of {steps}"
            f"(e.g. {', '.join(examples)}, etc.)"
        )
