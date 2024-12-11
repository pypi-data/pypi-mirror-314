"""app command for engineai CLI."""

from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from engineai.sdk.cli.utils import write_console
from engineai.sdk.dashboard.clients.mutation.app_api import AppAPI
from engineai.sdk.internal.clients.exceptions import APIServerError
from engineai.sdk.internal.exceptions import UnauthenticatedError

from .app_rule import rule


@click.group(name="app", invoke_without_command=False)
def app() -> None:
    """App commands."""


@app.command(
    "ls",
    help="""List all apps.

            \b
            WORKSPACE_SLUG: workspace to be listed.
            """,
)
@click.argument(
    "workspace_slug",
    required=True,
    type=str,
)
def list_workspace_app(workspace_slug: str) -> None:
    """List workspace apps.

    Args:
        workspace_slug: workspace to be listed.
    """
    api = AppAPI()
    try:
        apps = api.list_workspace_apps(workspace_slug)
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)

    if apps:
        slug = apps.get("slug")
        workspace_apps = apps.get("apps", [])

        if not workspace_apps:
            write_console("No apps found\n", 0)
            return

        console = Console()
        table = Table(
            title=f"Apps of workspace '{slug}'",
            show_header=False,
            show_edge=True,
        )
        for current_app in workspace_apps:
            table.add_row(current_app.get("slug"))
        console.print(table)


@app.command(
    "add",
    help="""Add new app.

            \b
            WORKSPACE_SLUG: workspace to be added.
            APP_SLUG: app to be added.
            APP_NAME: app name.
            """,
)
@click.argument(
    "workspace_slug",
    required=True,
    type=str,
)
@click.argument(
    "app_slug",
    required=True,
    type=str,
)
@click.argument(
    "app_name",
    required=True,
    type=str,
)
def add_app(workspace_slug: str, app_slug: str, app_name: str) -> None:
    """Add new app.

    Args:
        workspace_slug: workspace to be added.
        app_slug: app to be added.
        app_name: app name.
    """
    api = AppAPI()

    try:
        api.create_app(workspace_slug, app_slug, app_name)
        write_console(
            f"Successfully created app `{app_slug}` with name `{app_name}` within "
            f"workspace `{workspace_slug}`\n",
            0,
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


@app.command(
    "update",
    help="""Update current app.

        \b
        WORKSPACE_SLUG: workspace to be updated.
        APP_SLUG: app to be updated.
        """,
)
@click.argument(
    "workspace_slug",
    required=True,
    type=str,
)
@click.argument(
    "app_slug",
    required=True,
    type=str,
)
@click.option("-s", "--slug", type=str, default=None, help="new slug.")
@click.option("-n", "--name", type=str, default=None, help="new name.")
def update(
    workspace_slug: str, app_slug: str, slug: Optional[str], name: Optional[str]
) -> None:
    """Update current app.

    Args:
        workspace_slug: workspace to be updated.
        app_slug: app to be updated.
        new_app_slug: new app slug.
        new_app_name: new app name.
    """
    if slug is None and name is None:
        write_console(
            "Error: You must provide at least one of the following options:\n"
            "-s, --slug: new app slug\n"
            "-n, --name: new app name\n",
            1,
        )
        return
    api = AppAPI()
    try:
        api.update_app(
            workspace_slug=workspace_slug,
            app_slug=app_slug,
            new_app_slug=slug,
            new_app_name=name,
        )
        if slug is not None and name is not None:
            write_console(
                f"Successfully changed app `{app_slug}` within the workspace "
                f"`{workspace_slug}` to the new slug `{slug}` and the new name `{name}`\n",
                0,
            )
        elif slug is not None:
            write_console(
                f"Successfully changed app `{app_slug}` within the workspace "
                f"`{workspace_slug}` to the new slug `{slug}`\n",
                0,
            )
        else:
            write_console(
                f"Successfully changed app `{app_slug}` within the workspace "
                f"`{workspace_slug}` to the new name `{name}`\n",
                0,
            )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


app.add_command(rule)
