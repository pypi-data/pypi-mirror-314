"""Provide config for dashboard api."""

from typing import Dict
from typing import Final

DEFAULT_URL: Final[str] = "https://api.engineai.com"

AUTH_CONFIG: Final[Dict[str, Dict[str, str]]] = {
    "api.engineai.dev": {
        "device_code_url": "https://login.engineai.dev/oauth/device/code",
        "token_url": "https://login.engineai.dev/oauth/token",
        "client_id": "UxR3Nhc03f0MlURPGKK4W7uuj0m8ZH9t",
        "audience": "https://api.dystematic.dev",
    },
    "api.engineai.review": {
        "device_code_url": "https://login.engineai.review/oauth/device/code",
        "token_url": "https://login.engineai.review/oauth/token",
        "client_id": "2woAkEoVBZ2PyFRWMOW8nFvD0iaeNga5",
        "audience": "https://api.dystematic.review",
    },
    "api.engineai.com": {
        "device_code_url": "https://login.engineai.com/oauth/device/code",
        "token_url": "https://login.engineai.com/oauth/token",
        "client_id": "PeBZtJkx9cFmoDUY7v6wlXBVA1I2Wigd",
        "audience": "https://api.dystematic.com",
    },
    "localhost:4000": {
        "device_code_url": "https://dystematic-dev.eu.auth0.com/oauth/device/code",
        "token_url": "https://dystematic-dev.eu.auth0.com/oauth/token",
        "client_id": "UxR3Nhc03f0MlURPGKK4W7uuj0m8ZH9t",
        "audience": "http://api.dystematic.local:4000",
    },
}
