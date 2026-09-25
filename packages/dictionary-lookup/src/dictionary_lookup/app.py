"""Command-line entry point for Oxford lookup."""

from __future__ import annotations

import argparse
import logging
import re
from pathlib import Path

from .instance import run_single_instance
from .text import trim
from .window import run_window


def main() -> None:
    _configure_logging()
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


if __name__ == "__main__":
    main()
