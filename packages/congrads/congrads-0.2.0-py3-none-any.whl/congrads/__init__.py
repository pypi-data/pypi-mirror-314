# __init__.py
version = "0.2.0"

# Only expose the submodules, not individual classes
from . import constraints
from . import core
from . import datasets
from . import descriptor
from . import metrics
from . import networks
from . import utils

# Define __all__ to specify that the submodules are accessible, but not classes directly.
__all__ = [
    "constraints",
    "core",
    "datasets",
    "descriptor",
    "metrics",
    "networks",
    "utils",
]
