"""Translate objects to and from dicts produced/consumed by classify.run()."""

import logging
from typing import Dict, Type

# pylint: disable=cyclic-import
from .base import Adapter
from .dicom import DicomAdapter
from .fw import FWAdapter

__all__ = ["available_adapters"]

available_adapters: Dict[str, Type[Adapter]] = {
    "base": Adapter,
    "dicom": DicomAdapter,
    "flywheel": FWAdapter,
}

log = logging.getLogger(__name__)

try:
    from .nifti import NiftiFWAdapter

    available_adapters["nifti"] = NiftiFWAdapter
except NameError:
    log.error("Cannot use NiftiFWAdapter without fw-core-client")
