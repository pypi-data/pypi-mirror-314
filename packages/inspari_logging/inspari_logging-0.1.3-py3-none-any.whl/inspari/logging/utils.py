import os

"""
Utility functions for shared across logging modules.
"""

_logging_prefix = "prefix"
_logging_suffix = "suffix"
_logging_extras: dict[str, str] = {
    _logging_prefix: "",
    _logging_suffix: "",
}


def _resolve_environment() -> str:
    if "WEBSITE_SKU" in os.environ:
        return "azure"
    return "local"
