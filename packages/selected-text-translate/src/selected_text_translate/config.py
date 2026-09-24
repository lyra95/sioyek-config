"""Load local project settings from the workspace .env file."""

from __future__ import annotations

import os
from pathlib import Path
import re


_ENV_FILE = Path(__file__).resolve().parents[4] / ".env"
_VALID_KEY = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def load_dotenv(path: Path = _ENV_FILE) -> None:
    """Read KEY=VALUE entries without replacing existing environment values."""
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except FileNotFoundError:
        return

    for line in lines:
        entry = line.strip()
        if not entry or entry.startswith("#"):
            continue
        if entry.startswith("export "):
            entry = entry[len("export "):].lstrip()
        key, separator, value = entry.partition("=")
        key = key.strip()
        if not separator or not _VALID_KEY.fullmatch(key):
            continue

        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        elif " #" in value:
            value = value.split(" #", 1)[0].rstrip()
        os.environ.setdefault(key, value)
