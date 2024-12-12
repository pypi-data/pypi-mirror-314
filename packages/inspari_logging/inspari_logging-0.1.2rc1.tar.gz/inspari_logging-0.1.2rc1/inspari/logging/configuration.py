import json
import logging
import logging.config
import os

from colorama import Fore, Style
from colorama import init as colorama_init

from .utils import _resolve_environment, _logging_extras, _logging_prefix


"""
The configuration module hols generic logging configuration utilities.
"""


colorama_init()

os.system("color")  # requires for colors to work in Windows
logger = logging.getLogger(__name__)


_default_colors = {
    "app": Fore.BLUE,
    "server": Fore.YELLOW,
    "api": Fore.YELLOW,
    "worker": Fore.GREEN,
    "tasks": Fore.GREEN,
    "celery": Fore.GREEN,
    "db": Fore.MAGENTA,
    "psql": Fore.MAGENTA,
    "postgres": Fore.MAGENTA,
}


def is_gunicorn() -> bool:
    return "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")


def configure_prefix(name: str | None = None, color: str | None = None):
    """
    Configure a logging prefix with a name and (optionally) a color and environment. For example, if the name was
    "api" and the environment is "azure", the log would be something like,

    api|azure|INFO: This is a log message.

    where "api|azure" is yellow, unless another color is specified.
    """
    if name is None:
        return
    if color is None:
        color = _default_colors.get(name, "")  # type: ignore
    else:
        color = getattr(Fore, color.upper())
    prefix = f"{color}{name}|{_resolve_environment()}{Style.RESET_ALL}|"
    _logging_extras[_logging_prefix] = prefix


def configure_logging(config_path: str = "logging_config.json"):
    """
    Running in Gunicorn, the logging configuration is already set up. In other cases, the configuration is loaded from the config_path.
    """
    if is_gunicorn():
        return
    with open(config_path, "r") as f:
        config = json.load(f)
    logging.config.dictConfig(config)


def configure_logging_default(
    config_path: str = "logging_config.json",
    name: str | None = None,
    color: str | None = None,
):
    """
    A single entry point for logging configuration that invokes lower level functions with sane defaults.
    """
    configure_logging(config_path)
    configure_prefix(name, color)
