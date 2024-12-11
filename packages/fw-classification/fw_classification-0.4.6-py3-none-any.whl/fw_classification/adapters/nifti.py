"""Adapter for Flywheel file objects."""

from __future__ import annotations

import json
import logging
import os
import re
import tempfile
import typing as t

import backoff
from dotty_dict import Dotty
from fw_client import ClientError, FWClient, ServerError

from .deps import have_gtk
from .fw import META_EXCLUDE, FWAdapter
from .utils import FileInput

log = logging.getLogger(__name__)

# Hardset this to True since it would fail anyway on the Client/Server
# Error params to the backoffs.  If core-client isn't installed we'd get
# a NameError on module import anyway, this is caught in __init__.py
HAVE_CORE = True
HAVE_GTK = have_gtk()


if HAVE_GTK:
    # pylint: disable=unused-import

    from flywheel_gear_toolkit import GearToolkitContext

    # pylint: enable=unused-import

if t.TYPE_CHECKING:  # pragma: no cover
    from flywheel_gear_toolkit import GearToolkitContext


def get_retry_time() -> int:
    """Helper function to return retry time from env."""
    return int(os.getenv("NIFTI_RETRY_TIME", "30"))


B_FILE_RE = re.compile(r"^(.*)(.bval|.bvec)$")


@backoff.on_exception(backoff.expo, (ClientError, ServerError), max_time=get_retry_time)
@backoff.on_exception(backoff.expo, ValueError, max_time=get_retry_time)
def get_sidecar(  # pylint: disable=too-many-locals
    fw: FWClient, file: FileInput
) -> t.Tuple[str, t.Dict[str, t.Any], t.List[str]]:
    """Get hierarchy information."""
    parent_ref = file.hierarchy  # pylint: disable=unused-variable
    file_name = file.location.name
    log.info(f"Attempting to get sidecar for nifti {file_name}")
    candidates = fw.get(f"/{parent_ref.type}s/{parent_ref.id}").get("files", [])
    sidecar = None
    b_files = []
    # Loop through files in the acquisition
    for file_ in candidates:
        # Get bval/bvec if present.
        if file_["type"] in ["bval", "bvec"]:
            # Get file root
            try:
                root = B_FILE_RE.match(file_["name"]).groups()[0]  # type: ignore
                # Split original file name with root from above
                _, extension = file_name.split(root)
                # If the extension is a nifti, this file matches the
                #   is a bval/bvec for the original nifti.
                if extension in [".nii", ".nii.gz"]:
                    b_files.append(file_["name"])
            except (ValueError, AttributeError):
                continue

        # Get source code files (sidecar)
        if file_["type"] not in ["source code"]:
            continue
        try:
            # Get file root, continue if file doesn't end with `.json`
            name, _ = file_["name"].split(".json")
            # Split out root name, leaving only extension
            _, extension = file_name.split(name)
        except ValueError:
            continue
        # If extension is a nifti, this is our file.
        if extension in [".nii", ".nii.gz"]:
            sidecar = file_
            log.info(f"Found sidecar {file_.name}")
            break
    if sidecar is None:
        raise ValueError("Could not find NIfTI sidecar.")

    sidecar_json = {}
    fd, path = tempfile.mkstemp()
    os.close(fd)
    with open(path, "wb") as writer:
        resp = fw.get(
            f"/{parent_ref.type}s/{parent_ref.id}/files/{sidecar['name']}", stream=True
        )
        writer.write(resp.content)
    with open(path, "r", encoding="utf-8") as reader:
        sidecar_json = json.load(reader)
    os.unlink(path)
    return sidecar["name"], sidecar_json, b_files


def convert_bids_timings_to_dicom(bids_data):
    """Convert timing and other values in a loaded BIDS data dictionary to DICOM standard units for various modalities.

    :param bids_data: A dictionary containing BIDS sidecar data.
    """
    # Define a dictionary of BIDS keys to DICOM conversion functions
    conversion_map = {
        # MR specific conversions
        "RepetitionTime": lambda x: x * 1000,  # Convert seconds to milliseconds
        "EchoTime": lambda x: x * 1000,  # Convert seconds to milliseconds
        "InversionTime": lambda x: x * 1000,  # Convert seconds to milliseconds
        # CT specific conversions
        "ExposureTime": lambda x: x * 1000,  # Convert seconds to milliseconds
        # PET specific conversions
        "FrameDuration": lambda x: x * 1000,  # Convert seconds to milliseconds
    }

    # Convert the timings and other values
    for key, conversion_function in conversion_map.items():
        if key in bids_data:
            original_value = bids_data[key]
            converted_value = conversion_function(original_value)
            bids_data[key] = converted_value  # Update the dictionary in-place
            logging.info(f"Converted {key}: {original_value} -> {converted_value}")
        else:
            logging.debug(f"Key not found, skipping: {key}")

    return bids_data


class NiftiFWAdapter(FWAdapter):
    """Special adapter for Flywheel Nifti objects.

    `preprocess`: Pull info from sidecar.
    `postprocess`: Generate .metadata.json for nifti and sidecar.
    """

    def __init__(
        self,
        file: t.Dict[str, t.Any],
        gear_context: "GearToolkitContext",
        name: str = "",
        version: str = "",
    ) -> None:
        """Initialize nifti with sidecar empty."""
        super().__init__(file, gear_context, name=name, version=version)
        self.sidecar = ""
        self.b_files: t.List[str] = []

    def preprocess(self) -> t.Dict[str, t.Any]:
        """Populate hierarchy values."""
        i_dict = {"file": self.file.object.dict()}
        # Ensure file.info.header exists
        i_dict["file"].setdefault("info", {}).setdefault("header", {})
        if HAVE_CORE and self.fw:
            sidecar, sidecar_dict, b_files = get_sidecar(self.fw, self.file)
            sidecar_dict = convert_bids_timings_to_dicom(sidecar_dict)
            i_dict["file"]["info"]["header"].update({"dicom": sidecar_dict})
            self.sidecar = sidecar
            self.b_files = b_files
        return i_dict

    def postprocess(self, res: bool, out: Dotty) -> bool:
        """Populate sidecar meta."""
        if res:
            out.pop("file.info.header.dicom", None)
            metadata = out.to_dict()
            for key in META_EXCLUDE:
                metadata["file"].pop(key, None)
            self.gtk.metadata.update_file(self.file.dict(), **metadata["file"])
            file_ = metadata.get("file", {})
            for to_update in [self.sidecar, *self.b_files]:
                if to_update:
                    # Ignore when to_update == "", which can occur when a sidecar
                    # file does not exist
                    self.gtk.metadata.update_file(
                        to_update,
                        **{
                            key: file_.get(key, {})
                            for key in ["classification", "modality"]
                            if key in file_
                        },
                        container_type=self.file.hierarchy.type,
                    )
        return res
