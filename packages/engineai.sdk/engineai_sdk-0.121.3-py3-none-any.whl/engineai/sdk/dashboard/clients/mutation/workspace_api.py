"""Helper class to connect to Workspace API and obtain base types."""

import logging
from typing import Any
from typing import List
from typing import Optional

from engineai.sdk.internal.clients.api import APIClient

logger = logging.getLogger(__name__)
logging.getLogger("urllib3").propagate = False


class WorkspaceAPI(APIClient):
    """Workspace API class."""

    def update_workspace(
        self, slug: str, new_slug: Optional[str] = None, new_name: Optional[str] = None
    ) -> Any:
        """Update Workspace."""
        return self._request(
            query="""
                mutation updateWorkspace($input: UpdateWorkspaceInput!) {
                    updateWorkspace(input: $input) {
                        workspace {
                            slug
                            name
                        }
                    }
                }
                """,
            variables={
                "input": {"slug": slug, "newSlug": new_slug, "newName": new_name},
            },
        )

    def create_workspace(self, slug: str, name: str) -> Any:
        """Create Workspace."""
        return self._request(
            query="""
                mutation createWorkspace($input: CreateWorkspaceInput!) {
                    createWorkspace(input: $input) {
                        workspace {
                            slug
                            name
                        }
                    }
                }""",
            variables={"input": {"slug": slug, "name": name}},
        )

    def delete_workspace(self, workspace_name: str) -> Any:
        """Delete Workspace."""
        return self._request(
            query="""
                mutation deleteWorkspace($input: DeleteWorkspaceInput!) {
                    deleteWorkspace(input: $input)
                }
                """,
            variables={"input": {"slug": workspace_name}},
        )

    def list_workspace(self) -> List:
        """List all Workspaces."""
        return (
            self._request(
                query="""
                query {
                    viewer {
                        workspaces {
                            slug
                        }
                    }
                }"""
            )
            .get("data", {})
            .get("viewer", {})
            .get("workspaces", [])
        )

    def add_workspace_member(self, workspace_name: str, email: str, role: str) -> List:
        """Add memeber to workspace."""
        return self._request(
            query="""
                    mutation addWorkspaceMember($input: AddWorkspaceMemberInput!) {
                        addWorkspaceMember(input: $input) {
                            member {
                                workspace {
                                    slug
                                }
                                user {
                                    email
                                }
                                role
                            }
                        }
                    }""",
            variables={
                "input": {
                    "workspaceSlug": workspace_name,
                    "userEmail": email,
                    "role": role,
                }
            },
        ).get("data", {})

    def update_workspace_member(
        self, workspace_name: str, email: str, role: str
    ) -> List:
        """Update Workspace member."""
        return self._request(
            query="""
                    mutation updateWorkspaceMember(
                        $input: UpdateWorkspaceMemberInput!) {
                            updateWorkspaceMember(input: $input) {
                                member {
                                    workspace {
                                        slug
                                    }
                                    user {
                                        email
                                    }
                                    role
                                }
                            }
                        }""",
            variables={
                "input": {
                    "workspaceSlug": workspace_name,
                    "userEmail": email,
                    "role": role,
                }
            },
        ).get("data", {})

    def remove_workspace_member(self, workspace_name: str, email: str) -> List:
        """Remove workspace member."""
        return self._request(
            query="""
                    mutation removeWorkspaceMember(
                        $input: RemoveWorkspaceMemberInput!) {
                            removeWorkspaceMember(input: $input) {
                                member {
                                    workspace {
                                        slug
                                    }
                                }
                            }
                        }""",
            variables={"input": {"workspaceSlug": workspace_name, "userEmail": email}},
        ).get("data", {})

    def list_workspace_member(self, workspace_name: str) -> List:
        """List all workspaces members."""
        return (
            (
                self._request(
                    query="""
                        query ListWorkspacesMember ($slug: String!) {
                            workspace (slug: $slug){
                                slug
                                members {
                                    user {
                                        email
                                    }
                                    role
                                }
                            }
                        }""",
                    variables={"slug": workspace_name},
                )
            )
            .get("data", {})
            .get("workspace", {})
        )

    def transfer_workspace(self, workspace_name: str, email: str) -> List:
        """Transfer workspace to another user."""
        return self._request(
            query="""
                mutation transferWorkspace($input: TransferWorkspaceInput!) {
                    transferWorkspace(input: $input) {
                        member {
                            workspace {
                                slug
                            }
                            user {
                                email
                            }
                            role
                        }
                    }
                }""",
            variables={"input": {"workspaceSlug": workspace_name, "userEmail": email}},
        ).get("data", {})
