"""dashboard command for engineai CLI."""

from pathlib import Path
from typing import Generator
from typing import List
from typing import Optional
from typing import Tuple

import click
import inquirer
from rich.console import Console
from rich.table import Table

from engineai.sdk.cli.generator import ProjectAlreadyExistsError
from engineai.sdk.cli.generator import generate_template
from engineai.sdk.cli.generator import remove_temporary_files
from engineai.sdk.cli.utils import URL_HELP
from engineai.sdk.cli.utils import get_env_var
from engineai.sdk.cli.utils import run_env
from engineai.sdk.cli.utils import show_data_error
from engineai.sdk.cli.utils import write_console
from engineai.sdk.dashboard.clients.api import DashboardAPI
from engineai.sdk.dashboard.dashboard.dashboard import PLATFORM_URL
from engineai.sdk.dashboard.data.exceptions import DataValidationError
from engineai.sdk.internal.authentication.utils import MalformedURLError
from engineai.sdk.internal.authentication.utils import URLNotSupportedError
from engineai.sdk.internal.authentication.utils import add_url_into_env_file
from engineai.sdk.internal.authentication.utils import get_url
from engineai.sdk.internal.clients.exceptions import APIServerError
from engineai.sdk.internal.exceptions import UnauthenticatedError

DASHBOARD_CREATED_MSG = (
    "\nDashboard created! To publish your dashboard, navigate to "
    "`{}` folder and run `engineai dashboard publish` to publish.\n"
)

API_USER_ERRORS = ("NOT_FOUND", "FORBIDDEN")


def _show_dashboards(dashboards: List) -> None:
    """Show table for dashboards.

    Args:
        dashboards: dashboards object list.
    """
    if dashboards:
        console = Console()
        table = Table(
            title="Dashboards",
            show_header=True,
            show_edge=True,
        )
        table.add_column("Name")
        table.add_column("Slug")
        for dash in dashboards:
            table.add_row(dash.get("name"), dash.get("slug"))
        with console.pager():
            console.print(table)
    else:
        write_console("No dashboards found.\n", 0)


def _show_versions(version_list: Generator) -> None:
    """Show table for versions.

    Args:
        version_list: versions object generator.
        slug: dashboard slug.
    """
    console = Console()
    table = Table(
        title="Versions",
        show_header=True,
        show_edge=True,
    )
    table.add_column("Version")
    table.add_column("Active")
    for version in version_list:
        table.add_row(version.get("version"), str(version.get("active")))

    if len(table.rows) > 0:
        console.print(table)


def _show_runs(run_list: Generator) -> None:
    """Show table for runs.

    Args:
        run_list: runs object generator.
        slug: dashboard slug.
    """
    console = Console()
    table = Table(
        title="Runs",
        show_header=True,
        show_edge=True,
    )
    table.add_column("Run")
    table.add_column("Active")
    for run in run_list:
        table.add_row(run.get("slug"), str(run.get("active")))

    if len(table.rows) > 0:
        console.print(table)


def _prompt_version(version_list: Generator) -> Tuple[str, bool]:
    choices = []
    version_active = {}
    for item in version_list:
        choices.append(
            f"{item['version']} [Active]" if item["active"] else item["version"]
        )
        version_active[item["version"]] = item["active"]

    version_prompt = [
        inquirer.List(
            "version",
            message="Please select a version",
            choices=choices,
        )
    ]
    selected = inquirer.prompt(version_prompt)["version"].split()[0]
    return selected, version_active[selected]


def _prompt_run(run_list: Generator) -> str:
    choices = [
        f"{run['slug']} [Active]" if run["active"] else run["slug"] for run in run_list
    ]
    run_question = [
        inquirer.List(
            "run",
            message="Please select a run",
            choices=choices,
        )
    ]
    return inquirer.prompt(run_question)["run"].split()[0]


def _confirm_version_activation(version: str, active: bool) -> bool:
    if not active:
        msg = f"Version {version} is not active. Activate?"
        confirm_prompt = [
            inquirer.Confirm(
                "confirm",
                default=True,
                message=msg,
            )
        ]
        return inquirer.prompt(confirm_prompt)["confirm"]
    return True


def _confirm_activate(
    slug: str, version: str, run: str, activate_version: bool
) -> None:
    msg = (
        (
            f"You are about to activate dashboard `{slug}` "
            f"with version `{version}` and run `{run}`. Proceed?"
        )
        if activate_version
        else (
            f"You are about to activate run `{run}` from "
            f"dashboard `{slug}` (version: `{version}`) without activating "
            "its version. (Only available for preview). Proceed?"
        )
    )
    confirm_prompt = [
        inquirer.Confirm(
            "confirm",
            default=True,
            message=msg,
        )
    ]
    if not inquirer.prompt(confirm_prompt)["confirm"]:
        write_console("Activation cancelled.\n", 0)


def _validate_version(
    api: DashboardAPI, workspace_slug: str, app_slug: str, slug: str, version: str
) -> None:
    try:
        version_list = api.list_dashboard_versions(workspace_slug, app_slug, slug)
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)

    if version not in [item["version"] for item in version_list]:
        write_console(f"{slug} does not have version `{version}`\n", 1)


def _validate_run(
    api: DashboardAPI,
    workspace_slug: str,
    app_slug: str,
    slug: str,
    version: str,
    run: str,
) -> None:
    try:
        run_list = api.list_dashboard_runs(workspace_slug, app_slug, slug, version)
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)

    if run not in [item["slug"] for item in run_list]:
        write_console(f"{slug} version `{version}` does not have run `{run}`\n", 1)


def _validate_slug(
    api: DashboardAPI, workspace_slug: str, app_slug: str, slug: str
) -> None:
    try:
        dashboard_versions = api.list_dashboard_versions(workspace_slug, app_slug, slug)
        next(dashboard_versions)
    except StopIteration:
        write_console(f"Invalid dashboard slug `{slug}`\n", 1)
    except (APIServerError, UnauthenticatedError) as e:
        if e.args[-1] in API_USER_ERRORS:
            write_console(f"Invalid dashboard slug `{slug}`\n", 1)
        write_console(f"{e}\n", 1)


def _validate_app_slug(app_slug: Optional[str] = None) -> None:
    app_slug_var = get_env_var("APP_SLUG")
    if not app_slug_var and app_slug is None:
        write_console(
            "Please set an app. `engineai app ls` and `engineai app set`\n", 1
        )
    return app_slug or app_slug_var


def _validate_workspace_slug(workspace_slug: Optional[str] = None) -> None:
    workspace_slug_var = get_env_var("WORKSPACE_SLUG")
    if not workspace_slug_var and workspace_slug is None:
        write_console("Please set an workspace slug where the app belong\n", 1)
    return workspace_slug or workspace_slug_var


def _validate_inputs(
    api: DashboardAPI, slug: str, version: Optional[str], run: Optional[str]
) -> str:
    if version is None and run is not None:
        write_console("Unable to activate using a run without a version. ", 1)

    app_slug = _validate_app_slug()
    workspace_slug = _validate_workspace_slug()

    if not slug:
        write_console(
            "Please provide a dashboard slug. "
            "Example: `engineai dashboard -s some-dashboard`\n",
            1,
        )

    _validate_slug(api, workspace_slug, app_slug, slug)

    if version:
        _validate_version(api, workspace_slug, app_slug, slug, version)
    if run:
        _validate_run(api, workspace_slug, app_slug, slug, version, run)
    return workspace_slug, app_slug


@click.group(name="dashboard", invoke_without_command=False)
@click.option("-s", "--slug", type=str, default=None, help="Dashboard slug.")
@click.pass_context
def dashboard(ctx: click.Context, slug: str) -> None:
    """Dashboard commands."""
    ctx.ensure_object(dict)
    ctx.obj["SLUG"] = slug


@dashboard.command()
def init() -> None:
    """Create a simple and functional dashboard."""
    try:
        workspace_slug = click.prompt(
            "Enter the name of the workspace in which you would like to publish "
            "the dashboard.",
            default="workspace_slug",
            type=str,
            show_default=True,
        )

        app_slug = click.prompt(
            "Enter the name of the app in which you would like to publish "
            "the dashboard.",
            default="app_slug",
            type=str,
            show_default=True,
        )

        slug = click.prompt(
            "Name your dashboard", default="new_dashboard", type=str, show_default=True
        )

        is_new_project = generate_template(
            dashboard_slug=slug,
            app_slug=app_slug,
            workspace_slug=workspace_slug,
        )
        if is_new_project:
            write_console(DASHBOARD_CREATED_MSG.format(slug))
        else:
            write_console("Tutorial data has been successfully added to your project.")
    except ProjectAlreadyExistsError:
        write_console(
            "\nDashboard already exists! "
            "Please, remove it first or use another slug.\n",
            1,
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)
    finally:
        remove_temporary_files()


@dashboard.command()
@click.option(
    "-f",
    "--filename",
    type=str,
    default="main.py",
    help=("Overwrite default Dashboard file directory."),
)
@click.option(
    "-u",
    "--url",
    type=str,
    default=None,
    help=URL_HELP,
)
@click.option(
    "--skip-data",
    type=bool,
    is_flag=True,
    default=False,
    help=(
        "Skip the data processing and validation. Can only be used after "
        "the first complete run. It is useful to increase the dashboard performance."
    ),
)
@click.option(
    "--skip-browser",
    type=bool,
    is_flag=True,
    default=False,
    help=("Skip the browser opening after the dashboard is published."),
)
@click.option(
    "--exception-type-detail",
    type=click.Choice(["basic", "full"]),
    is_flag=False,
    default="basic",
    help=(
        "If the dashboard raises a type error, and the message comes "
        "with triple dots, this flag expands to the full information."
    ),
)
def publish(
    url: str,
    skip_data: bool,
    skip_browser: bool,
    filename: Optional[str] = None,
    exception_type_detail: str = "basic",
) -> None:
    """Log in the user and publish a dashboard into Dashboard API."""
    try:
        add_url_into_env_file(url=get_url(url))
        run_env(
            Path(filename).resolve(), skip_data, skip_browser, exception_type_detail
        )
    except (MalformedURLError, URLNotSupportedError, UnauthenticatedError) as e:
        write_console(f"\n{e}\n", 1)
    except DataValidationError as e:
        show_data_error(e)


@dashboard.command()
@click.option(
    "-a",
    "--app-slug",
    required=False,
    type=str,
    help="App where to look for dashboards.",
)
def ls(app_slug: str) -> None:
    """List all dashboards."""
    app_slug = _validate_app_slug(app_slug)
    api = DashboardAPI()
    try:
        dashboards = api.list_user_dashboards(app_slug)
        _show_dashboards(dashboards)
    except (APIServerError, UnauthenticatedError) as e:
        if e.args[-1] in API_USER_ERRORS:
            write_console(f"Invalid app slug `{app_slug}`\n", 1)
        write_console(f"{e}\n", 1)


@dashboard.command()
@click.option("-v", "--version", type=str, default=None, help="Dashboard version.")
@click.option("-r", "--run", type=str, default=None, help="Dashboard run.")
@click.pass_context
def activate(ctx: click.Context, version: Optional[str], run: Optional[str]) -> None:
    """Activate a dashboard manually or interactively."""
    api = DashboardAPI()
    workspace_slug, app_slug = _validate_inputs(api, ctx.obj["SLUG"], version, run)

    try:
        if version is None and run is None:
            version_list = api.list_dashboard_versions(
                workspace_slug, app_slug, ctx.obj["SLUG"]
            )
            version, version_active = _prompt_version(version_list)
            activate_version = _confirm_version_activation(version, version_active)

            run_list = api.list_dashboard_runs(
                workspace_slug, app_slug, ctx.obj["SLUG"], version
            )
            run = _prompt_run(run_list)

        elif run is None:
            activate_version = True
            run_list = api.list_dashboard_runs(
                workspace_slug, app_slug, ctx.obj["SLUG"], version
            )
            run = _prompt_run(run_list)
        else:
            activate_version = True

        _confirm_activate(ctx.obj["SLUG"], version, run, activate_version)
        api.activate_dashboard_by_slug(
            app_slug=app_slug,
            workspace_slug=workspace_slug,
            slug=ctx.obj["SLUG"],
            version=version,
            run=run,
            activate_version=activate_version,
        )

        write_console(
            f"Dashboard `{ctx.obj['SLUG']}` successfully activated. "
            "You can access it at "
            f"{PLATFORM_URL.get(api.url)}/{workspace_slug}/{app_slug}/"
            f"dashboard/{ctx.obj['SLUG']}\n"
            if activate_version
            else f"Dashboard `{ctx.obj['SLUG']}` run `{run}` successfully activated. "
            "You can preview it at "
            f"{PLATFORM_URL.get(api.url)}/{workspace_slug}/{app_slug}/"
            f"dashboard/{ctx.obj['SLUG']}"
            f"?dashboard-version={version}&dashboard-version-run={run}\n"
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


@dashboard.group()
@click.option("-v", "--version", type=str, default=None, help="Dashboard version.")
@click.pass_context
def versions(ctx: click.Context, version: str) -> None:  # pylint: disable=unused-argument
    """Dashboard versions subgroup commands."""
    ctx.obj["VERSION"] = version


@versions.command("ls")
@click.pass_context
def list_versions(ctx: click.Context) -> None:
    """List all versions for a given dashboard slug."""
    app_slug = _validate_app_slug()
    workspace_slug = _validate_workspace_slug()
    if not ctx.obj["SLUG"]:
        write_console(
            "Please provide a dashboard slug. "
            "Example: `engineai dashboard -s some-dashboard versions ls`\n",
            1,
        )
    api = DashboardAPI()
    try:
        version_list = api.list_dashboard_versions(
            workspace_slug, app_slug, ctx.obj["SLUG"]
        )
        _show_versions(version_list)
    except (APIServerError, UnauthenticatedError) as e:
        if e.args[-1] in API_USER_ERRORS:
            write_console(f"Invalid dashboard slug `{ctx.obj['SLUG']}`\n", 1)
        write_console(f"{e}\n", 1)


@versions.group()
@click.pass_context
def runs(ctx: click.Context) -> None:  # pylint: disable=unused-argument
    """Dashboard runs subgroup commands."""


@runs.command("ls")
@click.pass_context
def list_runs(ctx: click.Context) -> None:
    """List all runs for a given dashboard slug and version."""
    app_slug = _validate_app_slug()
    workspace_slug = _validate_workspace_slug()
    if not ctx.obj["SLUG"] or not ctx.obj["VERSION"]:
        write_console(
            "Please ensure both a slug and version are provided. "
            "Example: "
            "`engineai dashboard -s some-dashboard versions -v 0.0.0 runs ls`\n",
            1,
        )

    api = DashboardAPI()
    try:
        run_list = api.list_dashboard_runs(
            workspace_slug, app_slug, ctx.obj["SLUG"], ctx.obj["VERSION"]
        )
        _show_runs(run_list)
    except (APIServerError, UnauthenticatedError) as e:
        if e.args[-1] in API_USER_ERRORS:
            write_console(f"Invalid dashboard slug `{ctx.obj['SLUG']}`\n", 1)
        write_console(f"{e}\n", 1)
