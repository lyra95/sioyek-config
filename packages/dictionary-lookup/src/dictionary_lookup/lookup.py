"""Search a dictionary with the original word and all generated lemmas."""

from __future__ import annotations

from dataclasses import dataclass

from .engines.base import DictionaryEngine
from .lemmatization import possible_lemmas


@dataclass(frozen=True)
class LookupResult:
    requested_word: str
    matches: list["LookupMatch"]


@dataclass(frozen=True)
class LookupMatch:
    searched_word: str
    definitions: list[str]


def lookup_all_lemmas(engine: DictionaryEngine, word: str) -> LookupResult:
    """Search the original word and every POS lemma, returning all found entries."""
    candidates = possible_lemmas(word)
    ordered_candidates: list[str] = []
    seen: set[str] = set()
    for candidate in [word, *sorted(candidates - {word})]:
        normalized = candidate.casefold()
        if normalized not in seen:
            ordered_candidates.append(candidate)
            seen.add(normalized)
    matches: list[LookupMatch] = []
    errors: list[Exception] = []

    for candidate in ordered_candidates:
        try:
            definitions = engine.lookup(candidate)
        except Exception as exc:
            errors.append(exc)
            continue
        if definitions:
            matches.append(LookupMatch(candidate, definitions))

    if not matches and errors:
        raise errors[0]
    return LookupResult(word, matches)
