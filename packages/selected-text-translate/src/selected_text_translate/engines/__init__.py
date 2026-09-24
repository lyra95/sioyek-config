"""Available translation engines and their common interface."""

from .base import Translator
from .claude import ClaudeTranslator
from .codex import CodexTranslator
from .deepl import DeepLTranslator
from .google import GoogleTranslator

TRANSLATORS: dict[str, Translator] = {
    translator.name: translator
    for translator in (GoogleTranslator(), DeepLTranslator(), ClaudeTranslator(), CodexTranslator())
}

__all__ = ["TRANSLATORS", "Translator"]
