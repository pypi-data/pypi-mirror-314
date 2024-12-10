from __future__ import annotations

import hashlib
import logging
import os
import platform
import shutil
from pathlib import Path
from typing import TypeAlias

log = logging.getLogger(__name__)

_Path: TypeAlias = str | Path | os.PathLike


def get_relative_path(source: _Path, destination: _Path):
    # Get the absolute paths
    source = os.path.abspath(source)
    destination = os.path.abspath(destination)

    # Split the paths into components
    source_parts = source.split(os.sep)
    destination_parts = destination.split(os.sep)

    # Find the point where the paths diverge
    i = 0
    for i in range(min(len(source_parts), len(destination_parts))):
        if source_parts[i] != destination_parts[i]:
            break
    else:
        i += 1

    # Build the relative path
    up = os.sep.join([".." for _ in range(len(source_parts) - i - 1)])
    down = os.sep.join(destination_parts[i:])

    return Path(os.path.normpath(os.path.join(up, down)))


def find_symlinks(
    target_file: _Path,
    *search_directories: _Path,
    glob_pattern: str = "*",
):
    target_file = Path(target_file).resolve()
    symlinks: list[Path] = []

    for search_directory in search_directories:
        search_directory = Path(search_directory)
        for path in search_directory.rglob(glob_pattern):
            if path.is_symlink():
                try:
                    link_target = path.resolve()
                    if link_target.samefile(target_file):
                        symlinks.append(path)
                except FileNotFoundError:
                    # Handle broken symlinks
                    pass

    return symlinks


def compute_file_checksum(file_path: Path) -> str:
    """
    Calculate the SHA256 checksum of a file.

    Args:
        file_path (Path): The path to the file.

    Returns:
        str: The hexadecimal representation of the file's SHA256 checksum.
    """
    sha256_hash = hashlib.sha256()
    with file_path.open("rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def try_symlink_or_copy(
    file_path: Path,
    link_path: Path,
    target_is_directory: bool = False,
    relative: bool = True,
    remove_existing: bool = True,
):
    """
    Symlinks on Unix, copies on Windows.
    """

    # If the link already exists, remove it
    if remove_existing:
        try:
            if link_path.exists():
                if link_path.is_dir():
                    shutil.rmtree(link_path)
                else:
                    link_path.unlink(missing_ok=True)
        except Exception:
            log.warning(f"Failed to remove {link_path}", exc_info=True)
        else:
            log.debug(f"Removed {link_path=}")

    symlink_target = get_relative_path(link_path, file_path) if relative else file_path
    try:
        if platform.system() == "Windows":
            if target_is_directory:
                shutil.copytree(file_path, link_path)
            else:
                shutil.copy(file_path, link_path)
        else:
            link_path.symlink_to(
                symlink_target, target_is_directory=target_is_directory
            )
    except Exception:
        log.warning(
            f"Failed to create symlink or copy {file_path} to {link_path}",
            exc_info=True,
        )
        return False
    else:
        log.debug(f"Created symlink or copied {file_path} to {link_path}")
        return True
