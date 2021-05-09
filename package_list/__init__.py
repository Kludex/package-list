import importlib.metadata as importlib_metadata
import os
import re
import sys
from pathlib import Path
from platform import python_version
from typing import List

from stdlib_list import stdlib_list

__version__ = importlib_metadata.version(__name__)

__all__ = ["get_python_files", "find_python_packages"]

IMPORT_PATTERNS = [r"from (\w+)", r"^import (\w+)"]


def get_python_files(dir: Path) -> List[str]:
    python_files = []
    for root, _, filenames in os.walk(dir):
        for filename in filenames:
            if filename.endswith(".py"):
                python_files.append(os.path.join(root, filename))
    return python_files


def _find_python_packages_in_file(filename: Path) -> List[str]:
    packages = []
    with open(filename, "r") as file:
        content = file.read()
    for pattern in IMPORT_PATTERNS:
        matches = re.findall(pattern, content, re.MULTILINE)
        packages.extend([str(match) for match in matches])
    return list(set(packages))


def _find_python_packages_in_dir(dir: Path) -> List[str]:
    packages = []
    python_files = get_python_files(dir)
    for filename in python_files:
        packages.extend(_find_python_packages_in_file(filename))  # type: ignore
    return list(set(packages))


def find_python_packages(path: Path, include_std: bool = False) -> List[str]:
    if path.is_file():
        packages = _find_python_packages_in_file(path)
    else:
        packages = _find_python_packages_in_dir(path)
    packages.sort()
    if include_std:
        return packages
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    return [pkg for pkg in packages if pkg not in stdlib_list(python_version)]
