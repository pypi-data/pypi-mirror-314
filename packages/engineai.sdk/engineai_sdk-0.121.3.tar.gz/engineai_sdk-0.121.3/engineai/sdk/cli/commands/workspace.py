"""workspace command for engineai CLI."""

from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from engineai.sdk.cli.utils import write_console
from engineai.sdk.dashboard.clients.mutation.workspace_api import WorkspaceAPI
from engineai.sdk.internal.clients.exceptions import APIServerError
from engineai.sdk.internal.exceptions import UnauthenticatedError

from .workspace_member import member

WORKSPACE_ROLE = ["ADMIN", "MEMBER"]


@click.group(name="workspace", invoke_without_command=False)
def workspace() -> None:
    """Workspace commands."""


@workspace.command()
def ls() -> None:
    """List all workspace."""
    api = WorkspaceAPI()
    try:
        workspace_list = api.list_workspace()
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)

    if workspace_list:
        console = Console()
        table = Table(
            title="workspace",
            show_header=False,
            show_edge=True,
        )
        for current_workspace in workspace_list:
            table.add_row(current_workspace.get("slug"))
        console.print(table)
    else:
        write_console("No workspace found\n", 0)


@workspace.command("add")
@click.argument(
    "slug",
    required=True,
    type=str,
)
@click.argument(
    "name",
    required=True,
    type=str,
)
def add_workspace(slug: str, name: str) -> None:
    """Add new workspace.

    Args:
        workspace_name: workspace to be added.
    """
    api = WorkspaceAPI()
    try:
        api.create_workspace(slug, name)
        write_console(f"workspace `{slug}` added successfully\n", 0)
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


@workspace.command("rm")
@click.argument(
    "slug",
    required=True,
    type=str,
)
def remove_workspace(slug: str) -> None:
    """Remove workspace.

    Args:
        workspace_name: workspace to be removed.
    """
    api = WorkspaceAPI()
    try:
        api.delete_workspace(slug)
        write_console(f"workspace `{slug}` removed successfully\n", 0)
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


@workspace.command("update")
@click.argument(
    "workspace_slug",
    required=True,
    type=str,
)
@click.option("-s", "--slug", type=str, default=None, help="new slug.")
@click.option("-n", "--name", type=str, default=None, help="new name.")
def update(workspace_slug: str, slug: Optional[str], name: Optional[str]) -> None:
    """Update current workspace.

    Args:
        workspace_slug: workspace to be updated.
        slug: new workspace slug.
        name: new workspace name.
    """
    if slug is None and name is None:
        write_console(
            "Error: You must provide at least one of the following options:\n"
            "-s, --slug: new workspace slug\n"
            "-n, --name: new workspace name\n",
            1,
        )
        return
    api = WorkspaceAPI()
    try:
        api.update_workspace(slug=workspace_slug, new_slug=slug, new_name=name)
        if slug is not None and name is not None:
            write_console(
                f"workspace `{workspace_slug}` changed to new slug `{slug}` and "
                f"name `{name}` with success\n",
                0,
            )
        elif slug is not None:
            write_console(
                f"workspace `{workspace_slug}` changed to new slug `{slug}` with success\n",
                0,
            )
        else:
            write_console(
                f"workspace `{workspace_slug}` changed to new name `{name}` with success\n",
                0,
            )

    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


workspace.add_command(member)
