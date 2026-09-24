"""Codex CLI translation implementation."""

from __future__ import annotations

from .cli import CliTranslator


class CodexTranslator(CliTranslator):
    name = "Codex"
    executable = "codex"

    def translate(self, source: str) -> str:
        return self.run_cli([self.executable, "exec", "--ephemeral", "--skip-git-repo-check"], source)
