"""Command-line entry point for Oxford lookup."""

from __future__ import annotations

import argparse
import logging
import os
import re
import sys
from pathlib import Path

from .instance import run_single_instance
from .text import trim
from .window import run_window


def main() -> None:
    _configure_logging()
    _configure_tk_libraries()
    parser = argparse.ArgumentParser(description="Look up a word in Oxford or Naver English Dictionary.")
    parser.add_argument("--engine", choices=("oxford", "naver"), default="oxford")
    parser.add_argument("word", nargs="*", help="word or phrase to look up")
    args = parser.parse_args()
    word = trim(re.sub(r"\s+", " ", " ".join(args.word))) or "(no text selected)"
    engine = {"oxford": "Oxford", "naver": "Naver"}[args.engine]
    logging.info("Starting dictionary lookup (engine=%s, selected=%s)", args.engine, bool(args.word))
    try:
        run_single_instance("oxford-lookup", "word", word, lambda value, server: run_window(value, server, engine))
    except Exception:
        logging.exception("Dictionary lookup failed")
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
        # Logging must never prevent a lookup from opening.
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
