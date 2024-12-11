"""Auxiliary console methods."""

import datetime as dt
import json
import os
import runpy
import sys
import webbrowser
from pathlib import Path
from time import sleep
from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple
from urllib.parse import urlparse

import click
import dotenv
import pandas as pd
import requests
from rich.console import Console
from rich.table import Table

from engineai.sdk.dashboard.config import DASHBOARD_API_URL
from engineai.sdk.dashboard.data.exceptions import DataValidationError
from engineai.sdk.internal.authentication.auth0 import AUTH_CONFIG
from engineai.sdk.internal.authentication.auth0 import DEFAULT_URL

URL_HELP = (
    "URL of the EngineAI Platform API. Skipping option in the "
    "event you are using DASHBOARD_API_URL environment variable. "
    f"Default: {DEFAULT_URL}"
)


def get_env_var(key: str) -> Optional[str]:
    """Gets environment variables from the .env file."""
    dotenv_file = dotenv.find_dotenv(raise_error_if_not_found=True, usecwd=True)
    dotenv.load_dotenv(dotenv_file, override=True)
    return os.getenv(key)


def set_env_var(key: str, value: str) -> None:
    """Adds/updates environment variables into the .env file."""
    if not Path(".env").is_file():
        Path(".env").touch(exist_ok=True)

    dotenv_file = dotenv.find_dotenv(raise_error_if_not_found=True, usecwd=True)
    dotenv.load_dotenv(dotenv_file, override=True)
    dotenv.set_key(dotenv_file, key, value)


def write_console(message: str, exit_code: Optional[int] = None) -> None:
    """Writes a message to the console and exits with the given exit code if given.

    Args:
        message: The message to write to the console.
        exit_code: The exit code to use when exiting the program.
    """
    sys.stdout.write(message)
    if exit_code is not None:
        sys.exit(exit_code)


def run_env(
    file_path: Path, skip_data: bool, skip_browser: bool, exception_type_detail: str
) -> None:
    """Adds the root directory into the context and runs the python file."""
    dirpath = Path(file_path).resolve().parent

    sys.path.insert(0, str(dirpath))
    os.environ["SKIP_DATA"] = str(skip_data)
    os.environ["SKIP_OPEN_DASHBOARD"] = str(skip_browser)
    os.environ["EXCEPTION_TYPE_DETAIL"] = str(exception_type_detail)

    if file_path.exists():
        sys.stdout.write("\nPublishing Dashboard...\n")
        runpy.run_path(
            file_path.as_posix(),
            run_name=file_path.as_posix().split("/")[-1].split(".")[0],
        )
    else:
        sys.stdout.write(
            "By default we use `main.py` to publish but was not found in the current "
            "directory. Please make sure you are in the right directory or use "
            "`--filename` argument to indicate the new position or filename."
        )

    os.environ.pop("SKIP_DATA")
    os.environ.pop("SKIP_OPEN_DASHBOARD")
    os.environ.pop("EXCEPTION_TYPE_DETAIL")
    sys.path.remove(str(dirpath))


def authenticate(
    url: Optional[str] = None,
    force_auth: bool = False,
    force_token: bool = False,
) -> Tuple[str, str]:
    """Method that authenticates to the API to get the necessary publish tokens."""
    final_url = url or DASHBOARD_API_URL or ""
    if force_auth:
        final_url = final_url if final_url != "" else f"https://{list(AUTH_CONFIG)[-1]}"
    parsed_url = urlparse(final_url)
    if not parsed_url.netloc:
        msg = (
            f"URL ({final_url}) is malformed. Please use the default or insert a "
            "valid one."
        )
        raise ValueError(msg)
    auth_config: Dict[str, str] = AUTH_CONFIG.get(str(parsed_url.netloc), {})

    if not bool(auth_config):
        msg = (
            f"URL ({final_url}) is not supported. Please use the default or insert a "
            "valid one."
        )
        raise ValueError(msg)

    token = _handle_cli_auth(auth_config, force_token)
    return final_url, token


def show_data_error(data_error: DataValidationError) -> None:
    """Show formatted error message for DataValidationError.

    Args:
        data_error: DataValidationError object.
    """
    console = Console()
    data = data_error.args[0]
    widget_id = data_error.args[1]
    error_msg = str(data_error)
    df_table = _df_to_table(data)
    table = Table(
        title="Data Validation Error",
        show_header=False,
        show_edge=False,
        show_lines=True,
        style="bold red",
        title_style="bold red",
    )
    table.add_row("Widget ID:", widget_id, style="bold red")
    table.add_row("Error:", error_msg, style="bold red")
    table.add_row("Data snippet:", df_table, style="bold red")
    console.print()
    console.print(table)
    console.print()


def _df_to_table(
    data: pd.DataFrame,
    show_index: bool = True,
    index_name: str = "index",
    max_rows: int = 10,
    max_columns: int = 8,
) -> Table:
    """Convert a pandas.DataFrame obj into a rich.Table obj.

    Args:
        df: A Pandas DataFrame to be converted to a rich Table.
        show_index: Add a column with a row count to the table.
        index_name: The column name to give to the index column.
        max_rows: The maximum number of rows to display.
        max_columns: The maximum number of columns to display.

    Returns:
        Table: The rich Table instance passed, populated with the DataFrame values.
    """
    rich_table = Table()

    if len(data.index) > max_rows:
        data = pd.concat([data.head(max_rows // 2), data.tail(max_rows // 2)])
    if len(data.columns) > max_columns:
        data = data[
            data.columns[: max_columns // 2].tolist()
            + data.columns[-max_columns // 2 :].tolist()
        ]
        # add separator column for large tables
        data.insert(len(data.columns) // 2, "...", " ")

    if show_index:  # add index column
        index_name = str(index_name) if index_name else ""
        rich_table.add_column(index_name)

    for column in data.columns:
        rich_table.add_column(str(column))

    normalized_index = data.index.astype(str).tolist()
    row_values = data.to_numpy().tolist()
    col_length = len(data.columns) + 1 if show_index else len(data.columns)

    for i, (index, value_list) in enumerate(zip(normalized_index, row_values)):
        row = [str(index)] if show_index else []
        row += [str(value) for value in value_list]
        if i == len(data.index) // 2:
            # add separator row for large tables
            rich_table.add_row(*["..." for _ in range(col_length)])
        rich_table.add_row(*row)
    return rich_table


def _handle_cli_auth(
    auth_config: Dict[str, str],
    force_token: bool,
) -> str:
    token_file = _get_token_file_full_path(auth_config)
    if force_token:
        return _get_token(token_file, auth_config, _get_device_auth_code(auth_config))
    if (
        token_file.exists()
        and json.loads(token_file.read_text(encoding="utf-8"))["expires_at"]
        > dt.datetime.now().timestamp()
    ):
        token = str(json.loads(token_file.read_text(encoding="utf-8"))["access_token"])
    else:
        token = _get_token(token_file, auth_config, _get_device_auth_code(auth_config))

    return token


def _get_token_file_full_path(auth_config: Dict[str, str]) -> Path:
    return _get_token_directory() / Path(_get_token_filename(auth_config))


def _get_token_directory() -> Path:
    path: Path = Path.expanduser("~")
    path = path / Path(".engineai")

    if not Path.is_dir(path):
        Path.mkdir(path)

    return path


def _get_token_filename(auth_config: Dict[str, str]) -> str:
    filename = ".engineai_sdk"

    if not auth_config["audience"].endswith("com"):
        filename = f"{filename}_{auth_config['audience'].split('.')[-1]}"

    return filename


def _get_token(
    token_file: Path, auth_config: Dict[str, str], device_info: Dict[str, str]
) -> str:
    client_id = auth_config["client_id"]
    device_code_expires_at = dt.datetime.now() + dt.timedelta(
        seconds=float(device_info["expires_in"])
    )
    click.echo("Waiting for browser authentication ", nl=False)
    while dt.datetime.now() < device_code_expires_at:
        click.echo(".", nl=False)
        sleep(int(device_info["interval"]))

        response = requests.post(
            auth_config["token_url"],
            json={
                "client_id": client_id,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "device_code": device_info["device_code"],
            },
            timeout=60,
        )

        if response.status_code == 200:
            auth_token = response.json()
            auth_token["expires_at"] = (
                dt.datetime.now() + dt.timedelta(seconds=auth_token["expires_in"] - 5)
            ).timestamp()
            token_file.write_text(json.dumps(auth_token), encoding="utf-8")
            click.echo("\nAuthentication token obtained with success.")
            break

        if (
            response.status_code == 403
            and response.json()["error"] == "authorization_pending"
        ):
            continue

        click.echo(
            "Unable to obtain token. Response "
            f"(status_code='{response.status_code}', "
            f"reason='{response.reason}')."
        )
        raise click.Abort

    else:
        click.echo("Device code expired while waiting for web browser authentication.")
        raise click.Abort

    return str(auth_token["access_token"])


def _get_device_auth_code(auth_config: Dict[str, str]) -> Any:
    client_id = auth_config["client_id"]
    audience = auth_config["audience"]
    response = requests.post(
        auth_config["device_code_url"],
        json={
            "client_id": client_id,
            "audience": audience,
        },
        timeout=60,
    )
    if response.status_code != 200:
        click.echo(
            f"Unexpected status code (status_code={response.status_code}) "
            f"for url: {auth_config['device_code_url']}. "
            f"Response text: {response.text}"
        )
        raise click.Abort
    device_info = response.json()

    click.echo(
        "A web browser has been opened at "
        f"{device_info['verification_uri_complete']}. "
        "Please continue the login in the web browser. If the web browser fails to "
        "open please copy paste the respective url manually. Return here once "
        "you've logged in."
    )
    webbrowser.open(device_info["verification_uri_complete"])

    return device_info
