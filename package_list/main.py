import os
from pathlib import Path
from typing import Optional

from typer import Argument, Typer, echo

from package_list import find_python_packages

app = Typer(add_completion=False)


@app.command()
def list_packages(path: Optional[Path] = Argument(None, exists=True)):
    if path is None:
        path = Path(os.path.abspath(__file__))
    echo(find_python_packages(path))
