"""Command-line entry point for selected-text translation."""

from __future__ import annotations

import argparse
import re
import sys

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
    run_single_instance(
        "selected-text-translate",
        "text",
        text,
        lambda value, server: run_window(value, server, engine),
    )


if __name__ == "__main__":
    main()
