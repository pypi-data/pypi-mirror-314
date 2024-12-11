"""Configuration module."""

from pathlib import Path
from typing import Optional

from environs import Env

env = Env()
env.read_env(f"{Path.cwd()}/.env", recurse=False)

DASHBOARD_API_URL: Optional[str] = env.str("DASHBOARD_API_URL", None)

AUTH0_CONFIG_URL: Optional[str] = env.str("AUTH0_CONFIG_URL", None)

SKIP_DATA_VALIDATION = env.bool("SKIP_DATA_VALIDATION", False)
"""Skip dashboard validation."""

SKIP_DATA_VALIDATION = env.bool("SKIP_DATA_VALIDATION", False)
"""Skip dashboard validation."""

DASHBOARD_VERSION: Optional[str] = env.str("DASHBOARD_VERSION", None)
"""Set Dashboard Version."""

TOTAL_WORKERS: Optional[int] = env.int("TOTAL_WORKERS", 4)
"""Set Graph total workers."""
