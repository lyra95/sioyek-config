"""Shared process handling for local AI command-line translators."""

from __future__ import annotations

import subprocess

from .base import Translator


class CliTranslator(Translator):
    executable: str

    def run_cli(self, command: list[str], source: str) -> str:
        prompt = (
            "Translate the following text into Korean. Detect the source language automatically. "
            "Return only the Korean translation, preserving meaning and formatting.\n\n"
            f"{source}"
        )
        try:
            result = subprocess.run(
                [*command, prompt], capture_output=True, text=True, encoding="utf-8", timeout=180, check=False
            )
        except FileNotFoundError as exc:
            raise RuntimeError(f"Could not find {self.executable} on PATH. Install it and sign in first.") from exc
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(f"{self.name} did not finish within 3 minutes.") from exc
        if result.returncode:
            message = result.stderr.strip() or result.stdout.strip()
            raise RuntimeError(message or f"{self.name} exited with status {result.returncode}.")
        translation = result.stdout.strip()
        if not translation:
            raise RuntimeError(f"{self.name} returned an empty translation.")
        return translation
