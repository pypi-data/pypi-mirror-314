"""workspace member command for engineai CLI."""

import click
from rich.console import Console
from rich.table import Table

from engineai.sdk.cli.utils import write_console
from engineai.sdk.dashboard.clients.mutation.workspace_api import WorkspaceAPI
from engineai.sdk.internal.clients.exceptions import APIServerError
from engineai.sdk.internal.exceptions import UnauthenticatedError

WORKSPACE_ROLE = ["ADMIN", "MEMBER"]


@click.group()
def member() -> None:
    """Workspace member commands."""


@member.command(
    "add",
    help="""Add new member to workspace.

            \b
            SLUG: workspace to be updated.
            EMAIL: the user to be added to workspace.
            ROLE: role for the user in the workspace (ADMIN or MEMBER).
    """,
)
@click.argument(
    "slug",
    required=True,
    type=str,
)
@click.argument(
    "email",
    required=True,
    type=str,
)
@click.argument(
    "role",
    required=True,
    type=click.Choice(WORKSPACE_ROLE, case_sensitive=False),
)
def add_workspace_member(slug: str, email: str, role: str) -> None:
    """Add new member to workspace.

    Args:
        slug: workspace to be updated.
        email: user to be added to workspace.
        role: role for the user in the workspace (ADMIN or MEMBER).
    """
    api = WorkspaceAPI()
    member_role = role.upper()
    try:
        api.add_workspace_member(slug, email, member_role)
        write_console(
            f"User `{email}` added to workspace `{slug}` with role "
            f"`{member_role}` successfully\n",
            0,
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


@member.command(
    "update",
    help="""Update member role in workspace.

            \b
            SLUG: workspace to be updated.
            EMAIL: the user to be updated in the workspace.
            ROLE: new role for the user in the workspace (ADMIN or MEMBER).
    """,
)
@click.argument(
    "slug",
    required=True,
    type=str,
)
@click.argument(
    "email",
    required=True,
    type=str,
)
@click.argument(
    "role",
    required=True,
    type=click.Choice(WORKSPACE_ROLE, case_sensitive=False),
)
def update_workspace_member_role(slug: str, email: str, role: str) -> None:
    """Update member role in workspace.

    Args:
        slug: workspace to be updated.
        email: user to be updated in the workspace.
        role: new role for the user in the workspace (ADMIN or MEMBER).
    """
    api = WorkspaceAPI()
    member_role = role.upper()
    try:
        api.update_workspace_member(slug, email, member_role)
        write_console(
            f"User `{email}` updated to role `{member_role}` in workspace "
            f"`{slug}` with success\n",
            0,
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


@member.command(
    "rm",
    help="""Remove member from workspace.

            \b
            SLUG: workspace to be updated.
            EMAIL: the user to be removed from workspace.
        """,
)
@click.argument(
    "slug",
    required=True,
    type=str,
)
@click.argument(
    "email",
    required=True,
    type=str,
)
def remove_workspace_member(slug: str, email: str) -> None:
    """Remove member from workspace.

    Args:
        slug: workspace to be updated.
        email: user to be removed from workspace.
    """
    api = WorkspaceAPI()
    try:
        api.remove_workspace_member(slug, email)
        write_console(
            f"User `{email}` removed from workspace `{slug}` with success\n",
            0,
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


@member.command(
    "ls",
    help="""List all member in workspace.

            \b
            SLUG: workspace to be selected.
        """,
)
@click.argument(
    "slug",
    required=True,
    type=str,
)
def ls_workspace_member(slug: str) -> None:
    """List all member in workspace.

    Args:
        slug: workspace to be selected.
    """
    api = WorkspaceAPI()
    try:
        workspaces = api.list_workspace_member(slug)
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)

    if workspaces:
        slug = workspaces.get("slug")
        members = workspaces.get("members")
        console = Console()
        table = Table(
            title=f"Members of workspace '{slug}'",
            show_header=False,
            show_edge=True,
        )

        table.add_row("Member", "Role")
        table.add_section()
        for user in members:
            table.add_row(user.get("user").get("email"), user.get("role"))
        console.print(table)
    else:
        write_console("No workspace member found\n", 0)


@member.command(
    "transfer",
    help="""Transfer workspace to another member.

            \b
            SLUG: workspace to be updated.
            EMAIL: member to be new workspace owner.
        """,
)
@click.argument(
    "slug",
    required=True,
    type=str,
)
@click.argument(
    "email",
    required=True,
    type=str,
)
def transfer_workspace(slug: str, email: str) -> None:
    """Transfer workspace to another member.

    Args:
        slug: workspace to be updated.
        email: member to be new workspace owner.
    """
    api = WorkspaceAPI()
    try:
        api.transfer_workspace(slug, email)
        write_console(
            f"Workspace `{slug}` transferred to user `{email}` with " "success\n",
            0,
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)
