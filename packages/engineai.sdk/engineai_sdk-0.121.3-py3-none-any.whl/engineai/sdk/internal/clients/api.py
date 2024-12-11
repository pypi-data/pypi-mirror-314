"""Helper class to connect to Dashboard API and obtain base types."""

import json
import logging
import uuid
from typing import Any
from typing import Dict
from typing import Optional

import requests
import urllib3
from requests.adapters import CaseInsensitiveDict
from requests.adapters import HTTPAdapter

from engineai.sdk.internal.authentication.utils import get_token
from engineai.sdk.internal.authentication.utils import get_url
from engineai.sdk.internal.authentication.utils import is_valid_token
from engineai.sdk.internal.exceptions import UnauthenticatedError

from .exceptions import APIServerError

logger = logging.getLogger(__name__)
logging.getLogger("urllib3").propagate = False


class APIClient:
    """Class to generalize the API client."""

    def __init__(self, *, max_retries: int = 3) -> None:
        """Create connector to an API instance.

        Args:
            max_retries (int): maximum number of requests retries
        """
        self.__url = get_url()
        self.__token = get_token(self.__url)
        self.__session = self.__initialize_session(max_retries=max_retries)

    @property
    def url(self) -> str:
        """Get address of dashboard API."""
        return self.__url

    @property
    def token(self) -> str:
        """Get token of dashboard API."""
        if not is_valid_token(self.__token):
            self.__token = get_token(self.__url)
        return self.__token

    @staticmethod
    def __initialize_session(max_retries: int = 3) -> requests.Session:
        """Creates a HTTP/HTTPS session and returns."""
        retries = urllib3.Retry(
            total=max_retries,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["POST"],
        )
        adapter = HTTPAdapter(max_retries=retries)
        session = requests.Session()
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    def _request(
        self, *, query: str, variables: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Do a graphql request."""
        data = json.dumps(
            {"query": query, "variables": variables if variables is not None else {}}
        )
        headers: CaseInsensitiveDict = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = f"Bearer {self.token}"
        headers["x-request-id"] = str(uuid.uuid4())

        try:
            res = self.__session.post(self.__url, data=data, headers=headers)
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            error = e.response.content if e.response is not None else e
            raise APIServerError(
                request_id=headers["x-request-id"],
                error=str(error),
            ) from requests.exceptions.RequestException

        errors = res.json().get("errors")
        if errors:
            error_extensions = errors[0].get("extensions")
            if (
                error_extensions is not None
                and error_extensions.get("code") == "UNAUTHENTICATED"
            ):
                raise UnauthenticatedError

            raise APIServerError(
                request_id=headers["x-request-id"],
                error=errors[0].get("message"),
                error_code=error_extensions.get("code"),
            )
        return res.json()
