"""Interface implemented by each dictionary provider."""

from __future__ import annotations

from abc import ABC, abstractmethod


class DictionaryEngine(ABC):
    name: str
    window_title: str

    @abstractmethod
    def lookup(self, word: str) -> list[str]:
        """Return readable definition strings for the requested word."""

