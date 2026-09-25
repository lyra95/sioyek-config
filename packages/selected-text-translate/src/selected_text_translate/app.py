"""Command-line entry point for selected-text translation."""

from __future__ import annotations

import argparse
import logging
import re
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


if __name__ == "__main__":
    main()
