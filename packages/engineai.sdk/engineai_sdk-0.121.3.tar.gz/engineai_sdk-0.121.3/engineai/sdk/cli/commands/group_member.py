"""group member command for engineai CLI."""

import click
from rich.console import Console
from rich.table import Table

from engineai.sdk.cli.utils import write_console
from engineai.sdk.dashboard.clients.mutation.group_api import GroupAPI
from engineai.sdk.internal.clients.exceptions import APIServerError
from engineai.sdk.internal.exceptions import UnauthenticatedError


@click.group()
def member() -> None:
    """Group member commands."""


@member.command(
    "add",
    help="""Add group member.

        \b
        WORKSPACE_NAME: workspace to be updated.
        GROUP_NAME: app to be updated.
        EMAIL: user to be added.
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
    "email",
    required=True,
    type=str,
)
def add_group_member(
    workspace_name: str,
    group_name: str,
    email: str,
) -> None:
    """Add group member.

    Args:
        workspace_name: workspace to be updated.
        group_name: app to be updated.
        email: user to be added.
    """
    api = GroupAPI()
    try:
        api.add_group_member(
            workspace_name,
            group_name,
            email,
        )
        write_console(
            f"Added user `{email}` to the group `{group_name}` within "
            f"the `{workspace_name}` successfully\n",
            0,
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


@member.command(
    "rm",
    help="""Remove group member.

        \b
        WORKSPACE_NAME: workspace to be updated.
        GROUP_NAME: group to be updated.
        EMAIL: user to be removed.
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
    "email",
    required=True,
    type=str,
)
def remove_group_member(
    workspace_name: str,
    group_name: str,
    email: str,
) -> None:
    """Remove group member.

    Args:
        workspace_name: workspace to be updated.
        group_name: group to be updated.
        email: user to be removed.
    """
    api = GroupAPI()
    try:
        api.remove_group_member(workspace_name, group_name, email)
        write_console(
            f"User `{email}` removed from the group `{group_name}` within the "
            f"workspace `{workspace_name}` with success\n",
            0,
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


@member.command(
    "ls",
    help="""List group members.

        \b
        WORKSPACE_NAME: workspace to be selected.
        GROUP_NAME: group to be selected.
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
def list_group_member(
    workspace_name: str,
    group_name: str,
) -> None:
    """List group members.

    Args:
        workspace_name: workspace to be selected.
        group_name: group to be selected.
    """
    api = GroupAPI()
    try:
        group_members = api.list_group_member(workspace_name, group_name)
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)

    if group_members:
        group_name = group_members.get("slug")
        members = group_members.get("members")

        if not members:
            write_console("No group member found\n", 0)
            return

        console = Console()
        table = Table(
            title=f"Members of group '{group_name}'",
            show_header=False,
            show_edge=True,
        )

        table.add_row("User")
        table.add_section()

        for current_member in members:
            table.add_row(current_member.get("user").get("email"))
        console.print(table)
