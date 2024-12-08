from __future__ import annotations

PACKAGE_NAME: str = "tach"
TOOL_NAME: str = "tach"
CONFIG_FILE_NAME: str = TOOL_NAME
PACKAGE_FILE_NAME: str = "package"
ROOT_MODULE_SENTINEL_TAG: str = "<root>"

DEFAULT_EXCLUDE_PATHS = ["tests", "docs", ".*__pycache__", ".*egg-info"]

__all__ = [
    "PACKAGE_NAME",
    "TOOL_NAME",
    "CONFIG_FILE_NAME",
    "PACKAGE_FILE_NAME",
    "ROOT_MODULE_SENTINEL_TAG",
    "DEFAULT_EXCLUDE_PATHS",
]
