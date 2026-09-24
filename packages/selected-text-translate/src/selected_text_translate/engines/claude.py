"""Claude Code CLI translation implementation."""

from __future__ import annotations

from .cli import CliTranslator


class ClaudeTranslator(CliTranslator):
    name = "Claude"
    executable = "claude"

    def translate(self, source: str) -> str:
        return self.run_cli([self.executable, "-p"], source)
