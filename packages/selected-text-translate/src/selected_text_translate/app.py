"""Command-line entry point for selected-text translation."""

from __future__ import annotations

import argparse
import logging
import os
import re
import sys
from pathlib import Path

from .config import load_dotenv
from .instance import run_single_instance
from .window import run_window


ENGINES = {
    "google": "Google Translate",
    "deepl": "DeepL",
    "claude": "Claude",
    "codex": "Codex",
}


def main() -> None:
    _configure_logging()
    _configure_tk_libraries()
    load_dotenv()
    parser = argparse.ArgumentParser(description="Translate selected text into Korean.")
    parser.add_argument(
        "--engine",
        choices=tuple(ENGINES),
        default="google",
        help="default engine: google, deepl, claude, or codex (default: google)",
    )
    parser.add_argument("text", nargs="*", help="text to translate")
    args = parser.parse_args()
    text = re.sub(r"\s+", " ", " ".join(args.text)).strip() or "(no text selected)"
    engine = ENGINES[args.engine]
    logging.info("Starting translation (engine=%s, selected=%s)", args.engine, bool(args.text))
    try:
        run_single_instance(
            "selected-text-translate",
            "text",
            text,
            lambda value, server: run_window(value, server, engine),
        )
    except Exception:
        logging.exception("Selected-text translation failed")
        raise


def _configure_logging() -> None:
    """Record GUI-launch failures, which Finder otherwise discards."""
    try:
        log_path = Path.home() / "Library" / "Logs" / "sioyek-text-tools.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=log_path,
            encoding="utf-8",
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
            force=True,
        )
    except OSError:
        # Logging must never prevent a translation window from opening.
        pass


def _configure_tk_libraries() -> None:
    """Point uv's managed Python at the Tcl/Tk files it ships outside the venv.

    Tcl looks for its library under ``sys.prefix``, but uv keeps it with the
    interpreter, so every virtual environment needs the location spelled out.
    """
    base = Path(sys.base_prefix) / "lib"
    for variable, pattern, marker in (
        ("TCL_LIBRARY", "tcl[0-9]*", "init.tcl"),
        ("TK_LIBRARY", "tk[0-9]*", "tk.tcl"),
    ):
        for directory in sorted(base.glob(pattern), reverse=True):
            if (directory / marker).is_file():
                os.environ.setdefault(variable, str(directory))
                break


if __name__ == "__main__":
    main()
