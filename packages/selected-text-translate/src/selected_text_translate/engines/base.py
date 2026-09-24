"""Interface shared by translation engine implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Translator(ABC):
    """Translate text to Korean with a concrete provider."""

    name: str

    @abstractmethod
    def translate(self, source: str) -> str:
        """Return a Korean translation of source text."""

