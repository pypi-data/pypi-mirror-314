"""Dashboard Data Error."""

from typing import List
from typing import Optional

from engineai.sdk.dashboard.data.manager.interface import StaticDataType
from engineai.sdk.dashboard.exceptions import EngineAIDashboardError
from engineai.sdk.dashboard.utils import is_uuid


class DataValidationError(EngineAIDashboardError):
    """Dashboard Widget Data Error."""

    def __init__(
        self,
        data: StaticDataType,
        data_id: str,
        class_name: str,
        options: Optional[List[str]],
        error_string: str,
        function_name: Optional[str],
        *args: object,
    ) -> None:
        """Constructor for Dashboard Widget Data Error.

        Args:
            data: data to be validated.
            data_id: id for component (widget or route).
            class_name: widget type.
            options: options for widget.
            error_string: error string.
            function_name: function name.
        """
        super().__init__(
            data, data_id, class_name, options, error_string, function_name, *args
        )
        if not is_uuid(data_id):
            message = f"{class_name} with {data_id=}."
        else:
            message = (
                f"{class_name} error (to track which widget raised "
                "an error set the widget_id "
                f"example {class_name}(widget_id='example_id'))."
            )
        self.error_strings.append(message)
        if options:
            arguments = ", ".join([f"'{option}'" for option in options])
            self.error_strings.append(
                f"Data associated with method {function_name}({arguments})."
            )
        self.error_strings.append(error_string)


class DataProcessError(EngineAIDashboardError):
    """Dashboard Widget Data Process Error."""

    def __init__(
        self,
        data_id: str,
        class_name: str,
        options: Optional[List[str]],
        error_string: str,
        function_name: Optional[str],
        function_arguments: Optional[List[str]],
        *args: object,
    ) -> None:
        """Constructor for DataProcessError.

        Args:
            data_id: id for component.
            class_name: widget type.
            options: options for widget.
            error_string: error string.
            function_name: function name.
            function_arguments: function arguments.
        """
        super().__init__(
            data_id,
            class_name,
            options,
            error_string,
            function_name,
            function_arguments,
            *args,
        )
        # TODO: Validate if widget_id is uuid and add a message to inform user.
        message = f"{class_name} with {data_id=}."
        self.error_strings.append(message)
        if options and function_arguments:
            arguments = ", ".join(
                [
                    f"{argument}='{option}'"
                    for argument, option in zip(function_arguments, options)
                ]
            )
            self.error_strings.append(
                "Error while processing data from "
                f"method {function_name}({arguments})."
            )
        self.error_strings.append(error_string)


class DataAndOptionsDontMatchError(EngineAIDashboardError):
    """Dashboard Widget Data And Options Do Not Match Error."""

    def __init__(self) -> None:
        """Constructor for DataAndOptionsDontMatchError."""
        super().__init__()
        self.error_strings.append(
            "The number of combined options do not match with "
            "the data generated. Make sure that both options and data match."
        )


class DataInputsMismatchError(EngineAIDashboardError):
    """Dashboard Widget Data Inputs Mismatch Error."""

    def __init__(self, arguments: object, inputs: object, *args: object) -> None:
        """Constructor for DataInputsMismatchError."""
        super().__init__(arguments, inputs, *args)
        self.error_strings.append(
            "The number of function arguments does not match with the 'data_inputs' "
            f"feature: {arguments=} != {inputs=}. Please make sure that both match or "
            "please remove the 'data_inputs' option from the decorator."
        )


class DataRouteWithArgumentsError(EngineAIDashboardError):
    """Data Route With Arguments Error."""

    def __init__(self, *args: object) -> None:
        """Constructor for DataRouteWithArgumentsError."""
        super().__init__(*args)
        self.error_strings.append(
            "Arguments for Route Data are not supported. Please make sure that "
            "Route Data has no arguments."
        )
