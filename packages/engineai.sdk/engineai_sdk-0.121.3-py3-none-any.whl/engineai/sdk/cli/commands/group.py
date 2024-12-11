"""group command for engineai CLI."""

import click
from rich.console import Console
from rich.table import Table

from engineai.sdk.cli.utils import write_console
from engineai.sdk.dashboard.clients.mutation.group_api import GroupAPI
from engineai.sdk.internal.clients.exceptions import APIServerError
from engineai.sdk.internal.exceptions import UnauthenticatedError

from .group_member import member


@click.group(name="group", invoke_without_command=False)
def group() -> None:
    """Group commands."""


@group.command(
    "ls",
    help="""List all groups.

            \b
            WORKSPACE_NAME: workspace to be listed.
            """,
)
@click.argument(
    "workspace_name",
    required=True,
    type=str,
)
def list_workspace_group(workspace_name: str) -> None:
    """List workspace groups.

    Args:
        workspace_name: workspace to be listed.
    """
    api = GroupAPI()
    try:
        result = api.list_workspace_groups(workspace_name)
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)

    if result:
        slug = result.get("slug")
        workspace_groups = result.get("groups", [])

        if not workspace_groups:
            write_console("No groups found\n", 0)
            return

        console = Console()
        table = Table(
            title=f"Groups of workspace '{slug}'",
            show_header=False,
            show_edge=True,
        )
        for current_group in workspace_groups:
            table.add_row(current_group.get("slug"))
        console.print(table)


@group.command(
    "add",
    help="""Add new group.

        \b
        WORKSPACE_NAME: workspace to be added.
        GROUP_NAME: group to be added.
    """,
)
@click.argument(
    "workspace_name",
    required=True,
    type=str,
)
@click.argument(
    "group_name",
    required=True,
    type=str,
)
def add_group(workspace_name: str, group_name: str) -> None:
    """Add new group.

    Args:
        workspace_name: workspace to be added.
        group_name: group to be added.
    """
    api = GroupAPI()
    try:
        api.create_group(workspace_name, group_name)
        write_console(
            f"Group `{group_name}` added within the workspace `{workspace_name}` with "
            "success\n",
            0,
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


@group.command(
    "rm",
    help="""Delete current group.

        \b
        WORKSPACE_NAME: workspace contains group.
        GROUP_NAME: group to be deleted.
    """,
)
@click.argument(
    "workspace_name",
    required=True,
    type=str,
)
@click.argument(
    "group_name",
    required=True,
    type=str,
)
def delete(workspace_name: str, group_name: str) -> None:
    """Delete current group.

    Args:
        workspace_name: workspace contains group.
        group_name: group to be deleted.
    """
    api = GroupAPI()
    try:
        api.delete_group(workspace_name, group_name)
        write_console(
            f"Group `{group_name}` within the Workspace `{workspace_name}` "
            "deleted with success\n",
            0,
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


@group.command(
    "rename",
    help="""Update current app.

        \b
        WORKSPACE_NAME: workspace to be updated.
        GROUP_NAME: group to be updated.
        NEW_GROUP_NAME: group app name.
    """,
)
@click.argument(
    "workspace_name",
    required=True,
    type=str,
)
@click.argument(
    "group_name",
    required=True,
    type=str,
)
@click.argument(
    "new_group_name",
    required=True,
    type=str,
)
def update(workspace_name: str, group_name: str, new_group_name: str) -> None:
    """Update current app.

    Args:
        workspace_name: workspace to be updated.
        group_name: group to be updated.
        new_group_name: group app name.
    """
    api = GroupAPI()
    try:
        api.update_group(workspace_name, group_name, new_group_name)
        write_console(
            f"Group `{group_name}` within the workspace `{workspace_name}` renamed to "
            f"`{new_group_name}` with success\n",
            0,
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


group.add_command(member)
