"""Module to resolve includes of various types."""

import logging
import os
import shutil
import subprocess
import typing as t
from pathlib import Path

log = logging.getLogger(__name__)


def get_profile(search_dirs: t.List[Path], include: str) -> Path:
    """Get a profile from an include string.

    Includes can be one of the following:
    - Absolute path to an include
    - Relative path to an include in the same
      directory as the provided path
    - A git include with the format [git_repo]$[path/to/file]

    Args:
        search_dirs (List[Path]): Search paths for includes. The parent directory
            of this path will be used to resolve relative include.
        include (str): include string

    Returns:
        Path: path to profile
    """
    if "$" in include:
        return get_git_profile(include)
    include_path = Path(include)
    if include_path.is_absolute():
        return include_path
    for search_dir in search_dirs:
        resolve_path = search_dir / include_path
        if resolve_path.exists():
            return resolve_path

    searches = ", ".join(str(dir_) for dir_ in search_dirs)
    raise RuntimeError(f"Could not find profile {include}, search_dirs: {searches}")


def get_git_profile(include: str) -> Path:
    """Get a profile from a git source.

    Consumes includes with the format [git_repo]$[path/to/file].

    Args:
        include (str): Git source with the proper format.

    Returns:
        Path: path to profile

    Notes:
        * This repo must be public
        * Only works for 1-level deep git deps.
        i.e. if profile A includes git dep profile B
        profile B cannot have any git dependent profiles.
    """
    # Check for git executable
    git = shutil.which("git")
    if git:
        log.debug(f"Found git at {git}")
    else:
        raise RuntimeError(f'Need to have "git" installed to use git include {include}')
    tmp_dir = (
        Path(
            os.getenv("FW_CLASSIFICATION_TEMP_DIR")
            or "~/.cache/fw-classification/profiles"
        )
        .expanduser()
        .resolve()
    )
    tmp_dir.mkdir(parents=True, exist_ok=True)
    # Get repo and path to file in repo
    parts: t.List[str] = include.split("$")
    args: t.List[str] = ["git", "clone", "--depth", "1"]
    if len(parts) == 3:
        args.extend(["--branch", parts[2]])
    if len(parts) > 1:
        args.append(parts[0])
        path = parts[1]
    else:
        raise ValueError(f"Include {include} is improperly formatted")
    if tmp_dir.exists():
        log.debug("Git profiles dir exists, removing.")
        shutil.rmtree(tmp_dir)
    args.append(str(tmp_dir))
    # Clone the repo
    try:
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError as e:
        log.error(f"Could not clone git dependency {parts[0]}")
        raise RuntimeError from e
    # Return path
    return tmp_dir / path
