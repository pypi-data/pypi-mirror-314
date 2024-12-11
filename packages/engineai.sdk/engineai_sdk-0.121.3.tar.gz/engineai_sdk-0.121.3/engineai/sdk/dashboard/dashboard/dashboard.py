"""Spec for a Dashboard."""

import enum
import logging
import re
import sys
import webbrowser
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union
from typing import cast
from urllib.parse import urlparse

from environs import Env

from engineai.sdk.dashboard.clients import DashboardAPI
from engineai.sdk.dashboard.clients.activate_dashboard import ActivateDashboard
from engineai.sdk.dashboard.clients.storage import StorageConfig
from engineai.sdk.dashboard.dashboard.typings import DashboardContent
from engineai.sdk.dashboard.data import StorageType
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.internal.authentication.utils import get_url
from engineai.sdk.internal.clients.exceptions import APIServerError
from engineai.sdk.internal.url_config import PLATFORM_URL

from .enums import DashboardStatus
from .exceptions import DashboardDuplicatedPathsError
from .exceptions import DashboardEmptyContentError
from .exceptions import DashboardInvalidSlugError
from .exceptions import DashboardNoDashboardFoundError
from .exceptions import DashboardSkipDataCannotCreateRunError
from .graph.instance import Graph
from .page.page import Page
from .version.version import DashboardVersion

if TYPE_CHECKING:
    from engineai.sdk.dashboard.abstract.typing import PrepareParams

logger = logging.getLogger(__name__)


env = Env()


@dataclass
class DashboardResponse:
    """API response."""

    url_path: str
    dashboard_id: str
    version: Optional[str]
    run: Optional[str]
    app_slug: str
    workspace_slug: str
    dashboard_slug: str


class PublishMode(enum.Enum):
    """Dashboard Publish Mode.

    Attributes:
        DEFAULT: Default publish mode. The dashboard does not create new
            runs and automatically activates the published version.
        DEV: Development publish mode. The dashboard creates new
            runs and automatically activates the published version/run.
        DRAFT: Draft publish mode. The dashboard creates new
            runs but does not activate the published version/run.
        LIVE: Live publish mode. The dashboard creates new
            runs and automatically activates only the published run.

    **Version**: Set using the Dashboard *version* argument.

    **Run**: Automatically set based on the published date.
    """

    DEFAULT = "default"
    DEV = "dev"
    DRAFT = "draft"
    LIVE = "live"


class Dashboard:
    """Central component for managing layouts, widgets, cards.

    The Dashboard class is the central component for creating
    and managing dashboards. It serves as the container for various
    layout elements, widgets, and cards.
    """

    @type_check
    def __init__(
        self,
        *,
        slug: str,
        app_slug: str,
        workspace_slug: str,
        content: Union[List[Page], DashboardContent],
        name: Optional[str] = None,
        description: Optional[str] = None,
        last_available_data: Optional[Union[datetime, List[str]]] = None,
        status: Optional[DashboardStatus] = None,
        version: Optional[str] = None,
        skip_data: bool = False,
        storage_type: StorageType = StorageType.FILE_SHARE,
        publish_mode: PublishMode = PublishMode.DEFAULT,
    ) -> None:
        """Constructor for Dashboard.

        Args:
            slug: unique identifier for dashboard.
            app_slug: App slug where the dashboard will be published.
            workspace_slug: Workspace slug where the dashboard will be published.
            content: Dashboard content.
            name: Dashboard name to be displayed. Defaults to slug
                title case.
            description: Dashboard description. Markdown compliant
                string.
            last_available_data: Last available
                data for dashboard.
            status: Dashboard status.
            version: Dashboard version. By default, is None, can also be set
                using environment variable DASHBOARD_VERSION.
            skip_data: skip data processing. If True the publish process will
                only update the dashboard layout, if False the publish process will
                update the data and the layout.
            publish_mode: dashboard publish mode.
            storage_type: flag to set the storage type for the dashboard.
        """
        self._api_client = DashboardAPI()
        self.__slug: str = self._set_slug(slug)
        self.__name: str = name or slug.replace("_", " ").title()
        self.__pages = self.__generate_content(content=content)
        self.__skip_data = skip_data or env.bool("SKIP_DATA", False)
        self.__publish_mode = publish_mode
        self.__set_publish_mode()
        _reset_data_writes()
        self.__storage_type = storage_type

        if self.__skip_data and self.__create_run:
            raise DashboardSkipDataCannotCreateRunError

        self.__version: DashboardVersion = DashboardVersion(
            slug=self.__slug,
            last_available_data=last_available_data,
            status=status,
            version=version,
            create_run=self.__create_run,
        )

        self.__description = description
        self.__storage_config: Optional[StorageConfig] = None
        self.__skip_open_dashboard = env.bool("SKIP_OPEN_DASHBOARD", True)
        self.__app_slug = app_slug
        self.__workspace_slug = workspace_slug
        self.__publish()

    @property
    def is_single_page(self) -> bool:
        """Check if the dashboard has only one page."""
        return len(self.__pages) == 1

    def __set_publish_mode(self) -> None:
        """Set activate flag."""
        if self.__publish_mode == PublishMode.DEFAULT:
            self.__create_run = False
            self.__activate_version = True
            self.__activate_run = True
        elif self.__publish_mode == PublishMode.DEV:
            self.__create_run = True
            self.__activate_version = True
            self.__activate_run = True
        elif self.__publish_mode == PublishMode.DRAFT:
            self.__create_run = True
            self.__activate_version = False
            self.__activate_run = False
        else:
            self.__create_run = True
            self.__activate_version = False
            self.__activate_run = True

    @staticmethod
    def _set_slug(slug: str) -> str:
        """Set a new dashboard slug."""
        pattern = re.compile("^[a-z0-9-_]+$")

        if pattern.search(slug) is None or slug[-1] == "_":
            raise DashboardInvalidSlugError(slug=slug)

        return slug

    def __generate_content(
        self, content: Union[List[Page], DashboardContent]
    ) -> List[Page]:
        if isinstance(content, List) and len(content) == 0:
            raise DashboardEmptyContentError

        if isinstance(content, List) and all(
            isinstance(item, Page) for item in content
        ):
            return cast(List[Page], content)
        return [Page(name=self.__name, content=cast(DashboardContent, content))]

    def __publish(self) -> None:
        self.__validate_dashboard_exists()
        self.__prepare()
        self.__validate_pages()
        self.__publish_dashboard()

    def __publish_dashboard(self) -> None:
        dashboard_response = self._publish_in_api()
        if dashboard_response is not None:
            sys.stdout.write("Uploading Data.\n")
            self.__store_data(dashboard_response=dashboard_response)
            self.__activate_dashboard(
                dashboard_response=dashboard_response,
            )

            self.__finish_publish(dashboard_response=dashboard_response)

    def __finish_publish(
        self,
        dashboard_response: DashboardResponse,
    ) -> None:
        """Notify the user when the run ends."""
        full_url = self.__get_publish_url(dashboard_response=dashboard_response)
        sys.stdout.write("\n\nDashboard Successfully Published 🚀\n")
        sys.stdout.write(f"URL: {full_url}\n\n")
        self.__show_activate_command(dashboard_response=dashboard_response)
        if not self.__skip_open_dashboard:
            sys.stdout.write("Opening Dashboard in browser.....\n")
            webbrowser.open(full_url)

    def __get_publish_url(self, dashboard_response: DashboardResponse) -> str:
        platform_url = PLATFORM_URL.get(urlparse(self._api_client.url).netloc)
        url = (
            f"{platform_url}{dashboard_response.url_path}"
            if self._api_client.url is not None
            else None
        )

        if url is None:
            msg = "URL not found"
            raise ValueError(msg)

        return (
            url
            if self.__publish_mode in [PublishMode.DEFAULT, PublishMode.DEV]
            else (
                f"{url}?"
                f"dashboard-version={dashboard_response.version}&"
                f"dashboard-version-run={dashboard_response.run}"
            )
        )

    def __show_activate_command(
        self,
        dashboard_response: DashboardResponse,
    ) -> None:
        """Show the command to activate the dashboard."""
        if self.__publish_mode in [PublishMode.LIVE, PublishMode.DRAFT]:
            sys.stdout.write(
                "Dashboard published without activation. "
                "To activate please run this command:\n"
                f"engineai dashboard -s {dashboard_response.dashboard_slug} "
                f"activate -v {dashboard_response.version} "
                f"-r {dashboard_response.run}\n\n"
            )

    def _publish_in_api(self) -> Optional[DashboardResponse]:
        response = self._api_client.publish_dashboard(dashboard=self._build())
        return (
            DashboardResponse(
                url_path=response.get("url_path", None),
                dashboard_id=response.get("dashboard_id", None),
                version=response.get("version", None),
                run=response.get("run", None),
                workspace_slug=response.get("workspace_slug", None),
                app_slug=response.get("app_slug", None),
                dashboard_slug=response.get("dashboard_slug", None),
            )
            if response is not None
            else None
        )

    def __validate_pages(self) -> None:
        paths = set()
        for page in self.__pages:
            if page.path not in paths:
                paths.add(page.path)
            else:
                raise DashboardDuplicatedPathsError(page.path)
            page.validate()

    def __validate_dashboard_exists(self) -> None:
        if self.__skip_data:
            try:
                self._api_client.get_dashboard(
                    dashboard_slug=self.__slug.replace("_", "-"),
                    workspace_slug=self.__workspace_slug,
                    app_slug=self.__app_slug,
                    version=self.__version.version,
                )
            except APIServerError as e:
                raise DashboardNoDashboardFoundError(
                    slug=self.__slug,
                    workspace_slug=self.__workspace_slug,
                    app_slug=self.__app_slug,
                    version=self.__version.version,
                ) from e

    def __prepare(self) -> None:
        kwargs: PrepareParams = {
            "dashboard_slug": self.__slug,
            "storage_type": self.__storage_type,
        }
        if self.__version:
            self.__version.prepare(**kwargs)
        for page in self.__pages:
            page.prepare(**kwargs)

    def __key_value_config(
        self, dashboard_response: DashboardResponse
    ) -> StorageConfig:
        """Returns Dashboard default storage."""
        if self.__storage_config is None:
            self.__storage_config = self.__create_storage_config(dashboard_response)
        return self.__storage_config

    def __create_storage_config(
        self, dashboard_response: DashboardResponse
    ) -> StorageConfig:
        url = get_url()
        if url.endswith("/"):
            url = url[:-1]

        return StorageConfig(
            base_path=f"{url}/data-proxy/"
            f"workspace/{dashboard_response.workspace_slug}/"
            f"app/{dashboard_response.app_slug}/"
            f"dashboard/{dashboard_response.dashboard_slug}/"
            f"version/{dashboard_response.version}/"
            f"run/{dashboard_response.run}"
            f"/datastore/",
        )

    def __store_data(self, dashboard_response: DashboardResponse) -> None:
        if not self.__skip_data:
            kwargs: PrepareParams = {
                "dashboard_slug": self.__slug,
                "storage": self.__key_value_config(dashboard_response),
                "storage_type": self.__storage_type,
            }
            widgets = []
            routes = []
            for page in self.__pages:
                routes.append(page.route)
                widgets.append(page.widgets)
            Graph(widgets=widgets, routes=routes, **kwargs)

    def __activate_dashboard(self, dashboard_response: DashboardResponse) -> None:
        self._api_client.activate_dashboard(
            activate_dashboard=ActivateDashboard(
                dashboard_id=dashboard_response.dashboard_id,
                version=dashboard_response.version,
                activate_version=self.__activate_version,
                run=dashboard_response.run,
                activate_run=self.__activate_run,
            )
        )

    def __build_content(self) -> Dict[str, Any]:
        """Builds content for dashboard API."""
        return (
            {
                "layout": {"page": self.__pages[0].build()},
            }
            if self.is_single_page
            else {"pages": [page.build() for page in self.__pages]}
        )

    def _build(self) -> Dict[str, Any]:
        """Builds spec for dashboard API."""
        return {
            "name": self.__name,
            "slug": self.__slug.replace("_", "-"),
            "description": self.__description,
            "version": self.__version.build() if self.__version else None,
            "appSlug": self.__app_slug,
            "workspaceSlug": self.__workspace_slug,
            **self.__build_content(),
        }


def _reset_data_writes() -> None:
    if Path(".storage.txt").exists():
        Path(".storage.txt").unlink()
