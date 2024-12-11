"""Helper class to connect to Dashboard API and obtain base types."""

import logging
from typing import Any
from typing import List

from engineai.sdk.internal.clients.api import APIClient

logger = logging.getLogger(__name__)
logging.getLogger("urllib3").propagate = False


class GroupAPI(APIClient):
    """Group API class."""

    def create_group(self, workspace_name: str, group_name: str) -> Any:
        """Create Group."""
        return self._request(
            query="""
                mutation createGroup($input: CreateGroupInput!) {
                    createGroup(input: $input) {
                        group {
                            slug
                        }
                    }
                }""",
            variables={"input": {"slug": group_name, "workspaceSlug": workspace_name}},
        )

    def delete_group(self, workspace_name: str, group_name: str) -> Any:
        """Delete Group."""
        return self._request(
            query="""
                mutation deleteGroup($input: DeleteGroupInput!) {
                    deleteGroup(input: $input) {
                        group {
                            slug
                        }
                    }
                }
                """,
            variables={"input": {"slug": group_name, "workspaceSlug": workspace_name}},
        )

    def update_group(
        self, workspace_name: str, group_name: str, new_group_name: str
    ) -> Any:
        """Update Group."""
        return self._request(
            query="""
                mutation updateGroup($input: UpdateGroupInput!) {
                    updateGroup(input: $input) {
                        group {
                            slug
                        }
                    }
                }""",
            variables={
                "input": {
                    "slug": group_name,
                    "newSlug": new_group_name,
                    "workspaceSlug": workspace_name,
                }
            },
        )

    def add_group_member(
        self, workspace_name: str, group_name: str, email: str
    ) -> List:
        """Add memeber to group."""
        return self._request(
            query="""
                    mutation addGroupMember($input: AddGroupMemberInput!) {
                        addGroupMember(input: $input) {
                            member {
                                group {
                                    slug
                                }
                                user {
                                    email
                                }
                            }
                        }
                    }""",
            variables={
                "input": {
                    "workspaceSlug": workspace_name,
                    "groupSlug": group_name,
                    "userEmail": email,
                }
            },
        ).get("data", {})

    def remove_group_member(
        self, workspace_name: str, group_name: str, email: str
    ) -> List:
        """Remove group member."""
        return self._request(
            query="""
                    mutation removeGroupMember($input: RemoveGroupMemberInput!) {
                        removeGroupMember(input: $input) {
                            member {
                                group {
                                    slug
                                }
                                user {
                                    email
                                }
                            }
                        }
                    }""",
            variables={
                "input": {
                    "workspaceSlug": workspace_name,
                    "groupSlug": group_name,
                    "userEmail": email,
                }
            },
        ).get("data", {})

    def list_group_member(self, workspace_name: str, group_name: str) -> List:
        """List all group members."""
        return (
            (
                self._request(
                    query="""
                            query Group($workspaceSlug: String!, $slug: String!) {
                                group(workspaceSlug: $workspaceSlug, slug: $slug) {
                                    slug
                                    members {
                                        user {
                                            email
                                        }
                                    }
                                }
                            }""",
                    variables={"workspaceSlug": workspace_name, "slug": group_name},
                )
            )
            .get("data", {})
            .get("group", {})
        )

    def list_workspace_groups(self, workspace_slug: str) -> List:
        """List workspace groups."""
        return (
            self._request(
                query="""
                        query workspace($slug: String!) {
                            workspace(slug: $slug) {
                                slug
                                groups {
                                    slug
                                }
                            }
                        }""",
                variables={"slug": workspace_slug},
            )
            .get("data", {})
            .get("workspace", {})
        )
