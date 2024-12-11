"""Helper class to connect to Dashboard API and obtain base types."""

import logging
from typing import Any
from typing import Dict
from typing import Generator
from typing import List
from typing import Optional

from engineai.sdk.dashboard.clients.activate_dashboard import ActivateDashboard
from engineai.sdk.internal.clients.api import APIClient
from engineai.sdk.internal.clients.exceptions import DashboardAPINoVersionFoundError

logger = logging.getLogger(__name__)
logging.getLogger("urllib3").propagate = False


class DashboardAPI(APIClient):
    """Dashboard API Connector and Types."""

    def publish_dashboard(self, dashboard: Dict[Any, Any]) -> Optional[Dict[Any, Any]]:
        """Publish a Dashboard."""
        content = self._request(
            query="""
                mutation PublishDashboard ($input: DashboardInput!) {
                    publishDashboard(input: $input) {
                        run
                        id
                        version
                        url
                        slug
                        appSlug
                        workspaceSlug
                        warnings {
                            message
                        }
                    }
                }
            """,
            variables={"input": dashboard},
        )

        data = content.get("data", {}).get("publishDashboard", {})

        if data is None:
            return None

        return {
            "url_path": data.get("url"),
            "dashboard_id": data.get("id"),
            "version": data.get("version", None),
            "run": data.get("run", None),
            "app_slug": data.get("appSlug"),
            "workspace_slug": data.get("workspaceSlug"),
            "dashboard_slug": dashboard.get("slug", "").replace(" ", "-"),
        }

    def get_dashboard(
        self,
        dashboard_slug: str,
        app_slug: Optional[str],
        workspace_slug: Optional[str],
        version: Optional[str],
    ) -> None:
        """Get a dashboard."""
        return self._request(
            query="""
                query Dashboard(
                    $slug: String,
                    $appSlug: String!,
                    $workspaceSlug: String!,
                    $version: String) {
                        dashboard(
                            slug: $slug,
                            appSlug: $appSlug,
                            workspaceSlug: $workspaceSlug,
                            version: $version) {
                                name
                            }
                    }""",
            variables={
                "slug": dashboard_slug,
                "appSlug": app_slug,
                "workspaceSlug": workspace_slug,
                "version": version or "none",
            },
        )

    def get_dashboard_by_slug(
        self,
        dashboard_slug: str,
        version: str,
        run: str,
        app_slug: Optional[str],
        workspace_slug: Optional[str],
    ) -> Any:
        """Get a dashboard."""
        return (
            self._request(
                query="""
                    query Query(
                        $slug: String!,
                        $appSlug: String!,
                        $workspaceSlug: String!,
                        $version: String,
                        $run: String) {
                            dashboard(
                                slug: $slug,
                                appSlug: $appSlug,
                                workspaceSlug: $workspaceSlug,
                                version: $version,
                                run: $run) {
                                    id
                                }
                        }""",
                variables={
                    "slug": dashboard_slug,
                    "appSlug": app_slug,
                    "workspaceSlug": workspace_slug,
                    "version": version,
                    "run": run,
                },
            )
            .get("data", {})
            .get("dashboard", {})
            .get("id", "")
        )

    def list_user_dashboards(self, app_slug: str) -> List:
        """List user's dashboards."""
        return (
            self._request(
                query="""
                    query Apps($appSlug: String!) {
                        app(appSlug: $appSlug) {
                            dashboards {
                                name
                                slug
                            }
                        }
                    }""",
                variables={"appSlug": app_slug},
            )
            .get("data", {})
            .get("app", {})
            .get("dashboards", [])
        )

    def list_dashboard_versions(
        self, workspace_slug: str, app_slug: str, dashboard_slug: str
    ) -> Generator:
        """List dashboard versions."""
        dashboard_versions = self._get_dashboard_versions(
            workspace_slug, app_slug, dashboard_slug
        )
        yield from dashboard_versions

    def list_dashboard_runs(
        self, workspace_slug: str, app_slug: str, dashboard_slug: str, version: str
    ) -> Generator:
        """List dashboard version runs."""
        dashboard_versions = self._get_dashboard_versions(
            workspace_slug, app_slug, dashboard_slug
        )
        for dashboard_version in dashboard_versions:
            if dashboard_version.get("version") == version:
                yield from dashboard_version.get("runs", [])
                break

    def activate_dashboard(self, activate_dashboard: ActivateDashboard) -> None:
        """Activate a dashboard."""
        activate_dashboard_spec = activate_dashboard.build()

        return self._request(
            query="""
                mutation ActivateDashboard($input: ActivateDashboardInput!) {
                    activateDashboard(input: $input)
                }""",
            variables={"input": activate_dashboard_spec},
        )

    def activate_dashboard_by_slug(
        self,
        app_slug: str,
        workspace_slug: str,
        slug: str,
        version: str,
        run: str,
        activate_version: bool = True,
    ) -> None:
        """Activate a dashboard."""
        dashboard_id = self.get_dashboard_by_slug(
            slug, version, run, app_slug, workspace_slug
        )
        activate_dashboard_spec = ActivateDashboard(
            dashboard_id=dashboard_id,
            version=version,
            run=run,
            activate_version=activate_version,
        ).build()

        return self._request(
            query="""
                mutation ActivateDashboard($input: ActivateDashboardInput!) {
                    activateDashboard(input: $input)
                }""",
            variables={"input": activate_dashboard_spec},
        )

    def _get_dashboard_versions(
        self, workspace_slug: str, app_slug: str, dashboard_slug: str
    ) -> List:
        dashboard_versions = (
            self._request(
                query="""
                query DashboardVersions(
                    $workspaceSlug: String!,
                    $appSlug: String!,
                    $slug: String!) {
                        dashboardVersions(
                            workspaceSlug: $workspaceSlug,
                            appSlug: $appSlug,
                            slug: $slug) {
                                version
                                active
                                runs {
                                    slug
                                    active
                                }
                            }
                    }""",
                variables={
                    "workspaceSlug": workspace_slug,
                    "appSlug": app_slug,
                    "slug": dashboard_slug,
                },
            )
            .get("data", {})
            .get("dashboardVersions", [])
        )
        return dashboard_versions or []

    def _get_api_version(self) -> str:
        content = self._request(query="query Version {version { tag } }")

        if not self._version_content_valid(content):
            raise DashboardAPINoVersionFoundError

        return str(content.get("data").get("version").get("tag").replace("v", ""))

    @staticmethod
    def _version_content_valid(content: Dict[str, Any]) -> bool:
        return (
            "data" in content
            and "version" in content.get("data", {})
            and "tag" in content.get("data", {}).get("version", {})
        )
