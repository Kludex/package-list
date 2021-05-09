import os
import re
from pathlib import Path
from typing import List

__version__ = "0.1.0"

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


def find_python_packages(path: Path) -> List[str]:
    if path.is_file():
        return _find_python_packages_in_file(path)
    return _find_python_packages_in_dir(path)
