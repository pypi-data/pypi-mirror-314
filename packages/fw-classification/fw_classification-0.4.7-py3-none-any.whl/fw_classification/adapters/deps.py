"""Manage optional dependencies."""

import logging

log = logging.getLogger(__name__)

# pylint: disable=unused-import, import-outside-toplevel


def have_core() -> bool:  # pragma: no cover
    """Return True if fw-core-client is installed."""
    try:
        import fw_client  # noqa: F401

        HAVE_CORE = True
    except (ModuleNotFoundError, ImportError):  # pragma: no cover
        HAVE_CORE = False
        log.warning("Could not find fw-core-client, skipping Flywheel API calls.")
    return HAVE_CORE


def have_gtk() -> bool:  # pragma: no cover
    """Return True if flywheel-gear-toolkit is installed."""
    try:  # pragma: no cover
        from flywheel_gear_toolkit import GearToolkitContext  # noqa: F401

        HAVE_GTK = True  # pragma: no cover
    except (ModuleNotFoundError, ImportError):
        log.warning("Could not find flywheel-gear-toolkit.")
        HAVE_GTK = True
    return HAVE_GTK
