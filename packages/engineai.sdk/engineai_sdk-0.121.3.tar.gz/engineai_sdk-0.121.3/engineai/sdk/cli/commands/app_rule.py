"""app rule command for engineai CLI."""

import click
from rich.console import Console
from rich.table import Table

from engineai.sdk.cli.utils import write_console
from engineai.sdk.dashboard.clients.mutation.app_api import AppAPI
from engineai.sdk.internal.clients.exceptions import APIServerError
from engineai.sdk.internal.exceptions import UnauthenticatedError

APP_AUTHORIZATION_ROLE = ["ADMIN", "WRITE", "READ"]


@click.group()
def rule() -> None:
    """App rule commands."""


@rule.command(
    "add",
    help="""Add an authorization rule for the user in the app.

        \b
        WORKSPACE_SLUG: workspace to be updated.
        APP_SLUG: app to be updated.
        SUBJECT: the user/user group to apply new rules.
        ROLE: role for the user/user group in the app (ADMIN, WRITER OR READER).
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
    "subject",
    required=True,
    type=str,
)
@click.argument(
    "role",
    required=True,
    type=click.Choice(APP_AUTHORIZATION_ROLE, case_sensitive=False),
)
def add_app_authorization_rule(
    workspace_slug: str,
    app_slug: str,
    subject: str,
    role: str,
) -> None:
    """Add an authorization rule for the user/user group in the app.

    Args:
        workspace_slug: workspace to be updated.
        app_slug: app to be updated.
        subject: the user/user group to apply new rules.
        role: role for the user/user group in the app (ADMIN, WRITER OR READER).
    """
    if "@" in subject:
        user = subject
        user_group = None
    else:
        user = None
        user_group = subject

    authorization_role = role.upper()
    api = AppAPI()
    try:
        api.add_app_authorization_rule(
            workspace_slug,
            app_slug,
            user,
            user_group,
            authorization_role,
        )
        subject = f"user `{user}`" if user is not None else f"user group `{user_group}`"
        write_console(
            f"Successfully added new authorization rule for {subject} in app "
            f"`{app_slug}` within workspace `{workspace_slug}` with role "
            f"`{authorization_role}`\n",
            0,
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


@rule.command(
    "update",
    help="""Update app authorization rule to the user/user group in the app.

                \b
                WORKSPACE_SLUG: workspace to be updated.
                APP_SLUG: app to be updated.
                SUBJECT: the user/user group to apply new rules.
                ROLE: role for the user/user group in the app (ADMIN, WRITER OR READER).
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
    "subject",
    required=True,
    type=str,
)
@click.argument(
    "role",
    required=True,
    type=click.Choice(APP_AUTHORIZATION_ROLE, case_sensitive=False),
)
def update_app_authorization_rule(
    workspace_slug: str,
    app_slug: str,
    subject: str,
    role: str,
) -> None:
    """Update app authorization rule for user/user group in app.

    Args:
        workspace_slug: workspace to be updated.
        app_slug: app to be updated.
        subject: the user/user group to apply new rules.
        role: role for the user/user group in the app (ADMIN, WRITER OR READER).
    """
    if "@" in subject:
        user = subject
        user_group = None
    else:
        user = None
        user_group = subject

    authorization_role = role.upper()
    api = AppAPI()
    try:
        api.update_app_authorization_rule(
            workspace_slug,
            app_slug,
            user,
            user_group,
            authorization_role,
        )
        subject = f"user `{user}`" if user is not None else f"user group `{user_group}`"
        write_console(
            f"Successfully updated new authorization rule for {subject} in app "
            f"`{app_slug}` within workspace `{workspace_slug}` with role "
            f"`{authorization_role}`\n",
            0,
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


@rule.command(
    "rm",
    help="""Remove authorization rule to the user in the app.

                \b
                WORKSPACE_SLUG: workspace to be updated.
                APP_SLUG: workspace to be updated.
                SUBJECT: the user/user group to apply new rules.
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
    "subject",
    required=True,
    type=str,
)
def remove_app_authorization_rule(
    workspace_slug: str,
    app_slug: str,
    subject: str,
) -> None:
    """Remove authorization rule for user in app.

    Args:
        workspace_slug: workspace to be updated.
        app_slug: workspace to be updated.
        subject: the user/user group to apply new rules.
    """
    if "@" in subject:
        user = subject
        user_group = None
    else:
        user = None
        user_group = subject

    api = AppAPI()
    try:
        api.remove_app_authorization_rule(workspace_slug, app_slug, user, user_group)
        subject = f"user `{user}`" if user is not None else f"user group `{user_group}`"
        write_console(
            f"Successfully removed authorization rule for {subject} in app "
            f"`{app_slug}` within workspace `{workspace_slug}`\n",
            0,
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


@rule.command(
    "ls",
    help="""List app user authorization role.

        \b
        WORKSPACE_SLUG: workspace to be selected.
        APP_SLUG: app to be selected.
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
def list_app_authorization_rule(
    workspace_slug: str,
    app_slug: str,
) -> None:
    """List app user authorization role.

    Args:
        workspace_slug: workspace to be selected.
        app_slug: workspace to be selected.
    """
    api = AppAPI()
    try:
        app_rules = api.list_app_authorization_rule(workspace_slug, app_slug)
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)

    if app_rules:
        app_slug = app_rules.get("slug")
        authorization_rules = app_rules.get("authorizationRules")

        if not authorization_rules:
            write_console("No app member found\n", 0)
            return

        console = Console()
        table = Table(
            title=f"Rules of app '{app_slug}'",
            show_header=False,
            show_edge=True,
        )

        table.add_row("User/Group", "Role")
        table.add_section()

        for current_app in authorization_rules:
            subject = current_app.get("subject")
            name = subject.get("email", None) or subject.get("name", None)
            table.add_row(name, current_app.get("role"))
        console.print(table)
