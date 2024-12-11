"""Helper class to connect to APP API and obtain base types."""

import logging
from typing import Any
from typing import List
from typing import Optional

from engineai.sdk.internal.clients.api import APIClient

logger = logging.getLogger(__name__)
logging.getLogger("urllib3").propagate = False


class AppAPI(APIClient):
    """App API class."""

    def create_app(self, workspace_slug: str, app_name: str, title: str) -> Any:
        """Create App."""
        return self._request(
            query="""
                mutation CreateApp($input: CreateAppInput!) {
                    createApp(input: $input) {
                        app {
                            slug
                        }
                    }
                }""",
            variables={
                "input": {
                    "workspaceSlug": workspace_slug,
                    "slug": app_name,
                    "title": title,
                }
            },
        )

    def update_app(
        self,
        workspace_slug: str,
        app_slug: str,
        new_app_slug: Optional[str],
        new_app_name: Optional[str],
    ) -> Any:
        """Update App."""
        return self._request(
            query="""
                mutation UpdateApp($input: UpdateAppInput!) {
                    updateApp(input: $input) {
                        app {
                            slug
                            name
                        }
                    }
                }
                """,
            variables={
                "input": {
                    "workspaceSlug": workspace_slug,
                    "slug": app_slug,
                    "newSlug": new_app_slug,
                    "name": new_app_name,
                }
            },
        )

    def add_app_authorization_rule(
        self,
        workspace_slug: str,
        app_slug: str,
        user: Optional[str],
        user_group: Optional[str],
        role: str,
    ) -> List:
        """Add authorization rule for member or group in the app."""
        return self._request(
            query="""
                mutation addAuthorizationRule($input: AddAppAuthorizationRuleInput!){
                    addAppAuthorizationRule(input: $input) {
                        rule {
                            app {
                                slug
                                workspace {
                                    slug
                                }
                            }
                            role
                            subject{
                                ... on User {
                                    email
                                }
                                ... on Group {
                                    name: slug
                                }
                            }
                        }
                    }
                }""",
            variables={
                "input": {
                    "workspaceSlug": workspace_slug,
                    "appSlug": app_slug,
                    "subject": (
                        {"userEmail": user}
                        if user is not None
                        else {"groupSlug": user_group}
                    ),
                    "role": role,
                }
            },
        ).get("data", {})

    def update_app_authorization_rule(
        self,
        workspace_slug: str,
        app_slug: str,
        user: Optional[str],
        user_group: Optional[str],
        role: str,
    ) -> List:
        """Update authorization rule for member or group in the app."""
        return self._request(
            query="""
                mutation updateAuthorizationRule
                ($input: UpdateAppAuthorizationRuleInput!){
                    updateAppAuthorizationRule(input: $input) {
                        rule {
                            app {
                                slug
                                workspace {
                                    slug
                                }
                            }
                            role
                            subject{
                                ... on User {
                                    email
                                }
                                ... on Group {
                                    name: slug
                                }
                            }
                        }
                    }
                }""",
            variables={
                "input": {
                    "workspaceSlug": workspace_slug,
                    "appSlug": app_slug,
                    "subject": (
                        {"userEmail": user}
                        if user is not None
                        else {"groupSlug": user_group}
                    ),
                    "role": role,
                }
            },
        ).get("data", {})

    def remove_app_authorization_rule(
        self,
        workspace_slug: str,
        app_slug: str,
        user: Optional[str],
        user_group: Optional[str],
    ) -> List:
        """Remove workspace member."""
        return self._request(
            query="""
                mutation removeAuthorizationRule
                ($input: RemoveAppAuthorizationRuleInput!){
                    removeAppAuthorizationRule(input: $input) {
                        rule {
                            app {
                                slug
                                workspace {
                                    slug
                                }
                            }
                            role
                            subject{
                                ... on User {
                                    email
                                }
                                ... on Group {
                                    name: slug
                                }
                            }
                        }
                    }
                }""",
            variables={
                "input": {
                    "workspaceSlug": workspace_slug,
                    "appSlug": app_slug,
                    "subject": (
                        {"userEmail": user}
                        if user is not None
                        else {"groupSlug": user_group}
                    ),
                }
            },
        ).get("data", {})

    def list_app_authorization_rule(
        self,
        workspace_slug: str,
        app_slug: str,
    ) -> List:
        """List all apps authorization rules."""
        return (
            (
                self._request(
                    query="""
                        query ListAppRules($appSlug: String, $workspaceSlug: String){
                            app(appSlug: $appSlug, workspaceSlug: $workspaceSlug) {
                                workspace {
                                    slug
                                }
                                slug
                                authorizationRules {
                                    role
                                    subject{
                                        ... on User {
                                            email
                                        }
                                        ... on Group {
                                            name: slug
                                        }
                                    }
                                }
                            }
                        }""",
                    variables={"workspaceSlug": workspace_slug, "appSlug": app_slug},
                )
            )
            .get("data", {})
            .get("app", {})
        )

    def list_workspace_apps(self, workspace_slug: str) -> List:
        """List workspace apps."""
        return (
            self._request(
                query="""
                    query workspace($slug: String!) {
                        workspace(slug: $slug) {
                            slug
                            apps {
                                slug
                            }
                        }
                    }""",
                variables={"slug": workspace_slug},
            )
            .get("data", {})
            .get("workspace", {})
        )
