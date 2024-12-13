"""fw_classification module.

isort:skip_file
"""

import importlib.metadata

__version__ = importlib.metadata.version(__name__)

from .adapters import available_adapters  # noqa: F401
from .classify import Profile, run_classification  # noqa: F401
