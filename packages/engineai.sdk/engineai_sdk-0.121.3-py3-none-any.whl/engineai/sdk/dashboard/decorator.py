"""Decorator to check type of function parameters."""

import functools
import os
import sys
import warnings
from ast import literal_eval
from re import compile as re_compile
from typing import Any
from typing import cast

from beartype import beartype
from beartype._data.hint.datahinttyping import BeartypeableT
from beartype.roar import BeartypeCallHintParamViolation
from beartype.roar._roarwarn import BeartypeDecorHintPepDeprecationWarning
from rich.console import Console
from rich.markup import escape
from rich.table import Table

# beartype color codes
_ANSI_REGEX = re_compile(r"\033\[[0-9;?]*[A-Za-z]")


def type_check(func: BeartypeableT) -> BeartypeableT:
    """Decorator to check type of function parameters.

    Args:
        func (Callable): Function to be decorated.
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> BeartypeableT:
        with warnings.catch_warnings():
            warnings.simplefilter(
                "ignore", category=BeartypeDecorHintPepDeprecationWarning
            )
            try:
                decorated_func = beartype(func)
                return decorated_func(*args, **kwargs)
            except BeartypeCallHintParamViolation as e:
                if len(sys.argv) > 1:
                    # using CLI
                    return _parse_beartype_error(e, func.__annotations__, dict(kwargs))
                # using python script.py
                raise

    return cast(BeartypeableT, wrapper)


def _str_to_type(string: str) -> str:
    clean_string = string.strip()
    try:
        return str(type(literal_eval(clean_string)).__name__)
    except SyntaxError:
        return string


def _message_output(
    full_method_name: str, argument: str, expected_types: str, actual_type: str
) -> str:
    console = Console()
    table = Table(
        title="Type Validation Error",
        show_header=False,
        show_edge=False,
        show_lines=True,
        title_style="bold red",
    )
    table.add_row("Method:", escape(full_method_name), style="bold red")
    table.add_row("Argument:", escape(argument), style="bold red")
    table.add_row("Accepts:", escape(expected_types), style="bold red")
    table.add_row("Received:", escape(actual_type), style="bold red")
    console.print()
    console.print(table, overflow="fold")
    console.print()


def _parse_beartype_error(
    error: BeartypeCallHintParamViolation,
    annotations: dict,
    inputs: dict,
) -> None:
    """Parse Beartype error, print the error and exit program.

    Args:
        error: Beartype error.
        annotations: Function annotations.
        inputs: Function inputs.
    """
    error_msg = _ANSI_REGEX.sub("", error.args[0]).replace("'", '"')
    exception_type_detail = os.getenv("EXCEPTION_TYPE_DETAIL", "basic")

    try:
        full_method_name = error_msg.split("parameter")[0].split()[-1]
        argument = error_msg.split("parameter")[1].split()[0].split("=")[0]
        actual_type = (
            error_msg.split("parameter")[1].split("violates")[0].strip().split("=")[1]
        )
    except (KeyError, IndexError):
        sys.stdout.write(error_msg)
        sys.exit(1)

    _message_output(
        full_method_name,
        argument,
        str(annotations[argument]),
        (
            str(inputs[argument])
            if exception_type_detail == "full"
            else _str_to_type(actual_type)
        ),
    )
    sys.exit(1)
