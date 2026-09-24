"""Command-line entry point for Oxford lookup."""

from __future__ import annotations

import argparse
import re

from .instance import run_single_instance
from .text import trim
from .window import run_window


def main() -> None:
    parser = argparse.ArgumentParser(description="Look up a word in Oxford or Naver English Dictionary.")
    parser.add_argument("--engine", choices=("oxford", "naver"), default="oxford")
    parser.add_argument("word", nargs="*", help="word or phrase to look up")
    args = parser.parse_args()
    word = trim(re.sub(r"\s+", " ", " ".join(args.word))) or "(no text selected)"
    engine = {"oxford": "Oxford", "naver": "Naver"}[args.engine]
    run_single_instance("oxford-lookup", "word", word, lambda value, server: run_window(value, server, engine))


if __name__ == "__main__":
    main()
