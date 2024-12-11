"""Adapter for Flywheel file objects."""

from __future__ import annotations

import logging
import typing as t

from dotty_dict import Dotty

from .. import __version__
from .base import Adapter
from .deps import have_core, have_gtk
from .utils import FileInput

log = logging.getLogger(__name__)

HAVE_CORE = have_core()
HAVE_GTK = have_gtk()

if HAVE_CORE:
    from fw_client import ClientError, FWClient, ServerError

if HAVE_GTK:
    # pylint: disable=unused-import
    from flywheel_gear_toolkit import GearToolkitContext

    # pylint: enable=unused-import

if t.TYPE_CHECKING:  # pragma: no cover
    from flywheel_gear_toolkit import GearToolkitContext
    from fw_client import ClientError, FWClient, ServerError

HIERARCHY_ORDER = ["file", "acquisition", "session", "subject", "project"]
META_EXCLUDE = ["file_id", "type", "version", "origin", "size", "name"]
PARENT_INCLUDE = [
    # General values
    "label",
    "info",
    "uid",
    # Session values
    "age",
    "weight",
    # Subject values
    "sex",
    "cohort",
    "mlset",
    "ethnicity",
    "species",
    "strain",
    "code",
    "firstname",
    "lastname",
]


def get_hierarchy(i_dict: t.Dict[str, t.Any], fw: "FWClient", file: FileInput) -> None:
    """Get hierarchy information."""
    parent_ref = file.hierarchy
    parent = fw.get(f"/api/{parent_ref.type}s/{parent_ref.id}")
    parents_dict = parent["parents"]
    parent = {k: v for k, v in parent.items() if k in PARENT_INCLUDE}
    i_dict[parent_ref.type] = parent
    log.info(f"Running at {parent_ref.type} level")
    level = HIERARCHY_ORDER.index(parent_ref.type) + 1
    log.info(f"Pulling parent levels: {', '.join(HIERARCHY_ORDER[level:])}")
    orig_header = fw.headers["X-Accept-Feature"]
    fw.headers["X-Accept-Feature"] = "Safe-Redirect,Slim-Containers"
    for parent_type in HIERARCHY_ORDER[level:]:
        if parent_type in parents_dict:
            try:
                parent = fw.get(f"/api/{parent_type}s/{parents_dict[parent_type]}")
                parent = {k: v for k, v in parent.items() if k in PARENT_INCLUDE}
                log.info(f"Pulled {parent_type}, id: {parents_dict[parent_type]}")
                i_dict[parent_type] = parent
            except (ClientError, ServerError) as err:
                log.error(err)
    fw.headers["X-Accept-Feature"] = orig_header


class FWAdapter(Adapter):
    """Adapter for Flywheel objects.

    `preprocess`: Pull hierarchy information.
    `postprocess`: Generate .metadata.json
    """

    def __init__(
        self,
        file: t.Dict[str, t.Any],
        gear_context: "GearToolkitContext",
        name: str = "",
        version: str = "",
    ) -> None:
        """Initialize file and information to pull from API."""
        self.fw: t.Optional["FWClient"]
        f_input = FileInput(**file)
        super().__init__(f_input)
        if not (HAVE_GTK and gear_context):
            raise ValueError("Need `flywheel_gear_toolkit` to use this adapter.")
        self.gtk = gear_context
        if HAVE_CORE:
            try:
                api_key = gear_context.config_json["inputs"]["api-key"]["key"]
                self.fw = FWClient(
                    api_key=api_key,
                    client_name=(name or "fw-classification"),
                    client_version=(version or __version__),
                )
            except KeyError:
                log.warning("Could not find api-key.")
                self.fw = None
        else:
            self.fw = None

    def preprocess(self) -> t.Dict[str, t.Any]:
        """Populate hierarchy values."""
        i_dict = {
            "file": {
                "name": self.file.location.name,
                **self.file.object.dict(),
            }
        }
        if HAVE_CORE and self.fw:
            get_hierarchy(i_dict, self.fw, self.file)
        return i_dict

    def postprocess(self, res: bool, out: Dotty) -> bool:
        """Populate metadata for input file and parent container(s)."""
        if res:
            log.info("Generating .metadata.json from classification values.")
            metadata = out.to_dict()
            for key in HIERARCHY_ORDER[1:]:
                if key in metadata:
                    self.gtk.metadata.update_container(key, **metadata[key])
            for key in META_EXCLUDE:
                metadata["file"].pop(key, None)
            self.gtk.metadata.update_file(self.file.dict(), **metadata["file"])
        return res
