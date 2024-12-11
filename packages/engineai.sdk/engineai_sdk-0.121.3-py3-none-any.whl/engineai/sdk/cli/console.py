"""Cli main file."""

from typing import Optional

import click

from engineai.sdk import __version__
from engineai.sdk.cli.utils import URL_HELP
from engineai.sdk.cli.utils import write_console
from engineai.sdk.internal.authentication.utils import MalformedURLError
from engineai.sdk.internal.authentication.utils import URLNotSupportedError
from engineai.sdk.internal.authentication.utils import add_url_into_env_file
from engineai.sdk.internal.authentication.utils import authenticate
from engineai.sdk.internal.authentication.utils import get_url

from .commands import app as app_cmd
from .commands import dashboard as dashboard_cmd
from .commands import group as group_cmd
from .commands import workspace as workspace_cmd


@click.group()
@click.version_option(
    __version__,
    package_name="engineai.sdk",
    message="EngineAI's Platform SDK v%(version)s",
)
def process() -> None:
    """Platform SDK Command Line Interface."""


@process.command()
@click.option(
    "-u",
    "--url",
    type=str,
    default=None,
    help=URL_HELP,
)
def login(
    url: Optional[str] = None,
) -> None:
    """Log in the EngineAI API Authentication System."""
    try:
        url = get_url(url)
        add_url_into_env_file(url=url)
        authenticate(url, force_authentication=True)
    except (MalformedURLError, URLNotSupportedError) as e:
        write_console(f"\n{e}\n", 1)


process.add_command(dashboard_cmd.dashboard)
process.add_command(app_cmd.app)
process.add_command(workspace_cmd.workspace)
process.add_command(group_cmd.group)
