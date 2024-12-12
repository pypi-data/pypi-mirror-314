### IMPORTS
### ============================================================================
## Future

## Standard Library
import warnings

## Installed

## Application
from . import json
from . import utils

### CONSTANTS
### ============================================================================
ORJSON_AVAILABLE = utils.package_is_available("orjson")
MSGSPEC_AVAILABLE = utils.package_is_available("msgspec")


### DEPRECATED COMPATIBILITY
### ============================================================================
def __getattr__(name: str):
    if name == "jsonlogger":
        warnings.warn(
            "pythonjsonlogger.jsonlogger has been moved to pythonjsonlogger.json",
            DeprecationWarning,
        )
        return json
    raise AttributeError(f"module {__name__} has no attribute {name}")
