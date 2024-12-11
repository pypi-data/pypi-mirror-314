"""Auxiliary console methods."""

import datetime as dt
import json
import os
import sys
import webbrowser
from pathlib import Path
from time import sleep
from typing import Any
from typing import Dict
from typing import Optional
from urllib.parse import urlparse

import click
import dotenv
import jwt
import requests
from jwt.exceptions import PyJWTError

from engineai.sdk.dashboard.config import AUTH0_CONFIG_URL
from engineai.sdk.dashboard.config import DASHBOARD_API_URL
from engineai.sdk.internal.clients.exceptions import APIServerError

from .auth0 import AUTH_CONFIG
from .auth0 import DEFAULT_URL


class MalformedURLError(Exception):
    """Exception raised when the URL is malformed."""


class URLNotSupportedError(Exception):
    """Exception raised when the URL is not supported."""


def get_auth_config(url: str) -> Dict[str, str]:
    """Method that gets the auth config."""
    if AUTH0_CONFIG_URL is not None:
        return AUTH_CONFIG.get(urlparse(AUTH0_CONFIG_URL).netloc, {})
    return AUTH_CONFIG.get(urlparse(url).netloc, {})


def get_url(url: Optional[str] = None) -> str:
    """Method that validates the URL."""
    final_url = _get_url_from_variables(url)

    if not urlparse(final_url).netloc:
        msg = (
            f"URL ({final_url}) is malformed. "
            f"Please use the default url {DEFAULT_URL} or insert a valid one."
        )
        raise MalformedURLError(msg)
    if not bool(get_auth_config(final_url)):
        msg = (
            f"URL ({final_url}) is not supported. "
            f"Please use the default url {DEFAULT_URL} or insert a valid one."
        )
        raise URLNotSupportedError(msg)
    return final_url


def _get_url_from_variables(url: Optional[str]) -> str:
    if DASHBOARD_API_URL and url:
        sys.stdout.write(
            f"Using DASHBOARD_API_URL environment variable: "
            f"{DASHBOARD_API_URL} (ignoring 'url' argument).\n"
        )

    return DASHBOARD_API_URL or url or DEFAULT_URL


def add_url_into_env_file(url: str) -> None:
    """Method that adds DASHBOARD_API_URL environment variables into the .env file."""
    if not Path(".env").is_file():
        Path(".env").touch(exist_ok=True)

    dotenv_file = dotenv.find_dotenv(raise_error_if_not_found=True, usecwd=True)
    dotenv.load_dotenv(dotenv_file, override=True)
    dotenv.set_key(dotenv_file, "DASHBOARD_API_URL", url)
    dotenv.load_dotenv(dotenv_file, override=True)
    os.environ["DASHBOARD_API_URL"] = url


def authenticate(
    url: str,
    force_authentication: Optional[bool] = False,
) -> str:
    """Method that authenticates to the API to get the necessary publish tokens."""
    auth_config = get_auth_config(url)
    token_file = _get_token_file_full_path()

    if force_authentication:
        return _get_token(token_file, auth_config, _get_device_auth_code(auth_config))
    if not _is_current_token_valid(token_file):
        return _refresh_access_token(auth_config, token_file)
    return str(json.loads(token_file.read_text(encoding="utf-8"))["access_token"])


def _is_current_token_valid(token_file: Any) -> bool:
    return (
        token_file.exists()
        and json.loads(token_file.read_text(encoding="utf-8"))["expires_at"]
        > dt.datetime.now().timestamp()
    )


def _get_token_file_full_path() -> Path:
    return _get_token_directory() / ".engineai_sdk"


def _get_token_directory() -> Path:
    path: Path = Path.expanduser(Path("~"))
    path = path / ".engineai"

    if not Path.is_dir(path):
        Path.mkdir(path)

    return path


def _get_token(
    token_file: Path, auth_config: Dict[str, str], device_info: Dict[str, str]
) -> str:
    client_id = auth_config["client_id"]
    device_code_expires_at = dt.datetime.now() + dt.timedelta(
        seconds=float(device_info["expires_in"])
    )
    click.echo("Waiting for browser confirmation", nl=False)
    while dt.datetime.now() < device_code_expires_at:
        click.echo(".", nl=False)
        sleep(int(device_info["interval"]))

        response = requests.post(
            auth_config["token_url"],
            json={
                "client_id": client_id,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "device_code": device_info["device_code"],
            },
            timeout=60,
        )

        if response.status_code == 200:
            auth_token = response.json()
            auth_token["expires_at"] = (
                dt.datetime.now() + dt.timedelta(seconds=auth_token["expires_in"] - 5)
            ).timestamp()
            token_file.write_text(json.dumps(auth_token), encoding="utf-8")
            click.echo("\nAuthentication token obtained with success.")
            break

        if (
            response.status_code == 403
            and response.json()["error"] == "authorization_pending"
        ):
            continue

        click.echo(
            "Unable to obtain token. Response "
            f"(status_code='{response.status_code}', "
            f"reason='{response.reason}')."
        )
        raise click.Abort

    else:
        click.echo("Device code expired while waiting for web browser authentication.")
        raise click.Abort

    return str(auth_token["access_token"])


def _refresh_access_token(auth_config: Dict[str, str], token_file: Path) -> str:
    refresh_token = json.loads(token_file.read_text(encoding="utf-8")).get(
        "refresh_token"
    )

    response = requests.post(
        auth_config["token_url"],
        json={
            "client_id": auth_config["client_id"],
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
        timeout=60,
    )

    if response.status_code == 200:
        auth_token = response.json()
        auth_token["expires_at"] = (
            dt.datetime.now() + dt.timedelta(seconds=auth_token["expires_in"] - 5)
        ).timestamp()
        if "refresh_token" not in auth_token:
            auth_token["refresh_token"] = refresh_token
        token_file.write_text(json.dumps(auth_token), encoding="utf-8")
        return str(auth_token["access_token"])
    return _get_token(token_file, auth_config, _get_device_auth_code(auth_config))


def get_access_token_with_refresh_token(url: str, refresh_token: str) -> str:
    """Method that get access token with refresh token."""
    auth_config = get_auth_config(url)
    response = requests.post(
        auth_config["token_url"],
        json={
            "client_id": auth_config["client_id"],
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
        timeout=60,
    )

    if response.status_code == 200:
        auth_token = response.json()
        return str(auth_token["access_token"])
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise APIServerError(
            request_id=response.headers.get("X-Request-ID", ""),
            error=f"HTTP error occurred: {err!s}",
        ) from err


def get_token(url: str) -> str:
    """Set auth token."""
    # TODO: this is currently a workaround in order to be able to get a token
    # from the environment in a remote resource (i.e: a POD), that will
    # run a Dashboard and it won't be able to use Auth0's "Device Authorization
    # Flow". Ideally, for these cases, we use the "Client Credentials Flow"
    # (Machine to Machine), by sending a client secret, so that a token can be
    # obtained without a user having to authenticate in the web browser.
    # For more information, refer to:
    # https://auth0.com/docs/get-started/authentication-and-authorization-flow
    if "DASHBOARD_API_REFRESH_TOKEN" in os.environ:
        token = get_access_token_with_refresh_token(
            url,
            os.environ["DASHBOARD_API_REFRESH_TOKEN"],
        )
    elif "DASHBOARD_API_TOKEN" in os.environ:
        token = os.environ["DASHBOARD_API_TOKEN"]
    else:
        token = authenticate(url, force_authentication=False)
        os.environ["DASHBOARD_API_TOKEN"] = token

    return token


def is_valid_token(token: str) -> bool:
    try:
        information = jwt.decode(token, options={"verify_signature": False})
    except PyJWTError:
        return False
    else:
        if "exp" not in information:
            return False

        return (
            dt.datetime.fromtimestamp(float(information.get("exp", 0)))
            > dt.datetime.now()
        )


def _get_device_auth_code(auth_config: Dict[str, str]) -> Any:
    client_id = auth_config["client_id"]
    audience = auth_config["audience"]
    response = requests.post(
        auth_config["device_code_url"],
        json={
            "client_id": client_id,
            "audience": audience,
            "scope": "offline_access",
        },
        timeout=60,
    )
    if response.status_code != 200:
        click.echo(
            f"Unexpected status code (status_code={response.status_code}) "
            f"for url: {auth_config['device_code_url']}. "
            f"Response text: {response.text}"
        )
        raise click.Abort
    device_info = response.json()
    click.echo(
        f"Validate the following code in the browser: {device_info['user_code']}\n\n"
        f"Opening URL at {device_info['verification_uri_complete']} "
        "(copy if it does not open automatically)\n"
    )
    webbrowser.open(device_info["verification_uri_complete"])

    return device_info
