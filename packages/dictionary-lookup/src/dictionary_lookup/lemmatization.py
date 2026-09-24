"""WordNet-based candidate generation for dictionary searches."""

from __future__ import annotations

import threading

import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer


_LEMMATIZER = WordNetLemmatizer()
_WORDNET_READY = False
_WORDNET_LOCK = threading.Lock()
_PARTS_OF_SPEECH = ("n", "v", "a", "r", "s")


def _ensure_wordnet() -> None:
    global _WORDNET_READY
    if _WORDNET_READY:
        return

    with _WORDNET_LOCK:
        if _WORDNET_READY:
            return
        try:
            wordnet.ensure_loaded()
        except LookupError:
            if not nltk.download("wordnet", quiet=True):
                raise RuntimeError(
                    "NLTK WordNet data is unavailable. Run "
                    "'uv run --project packages/dictionary-lookup python -m nltk.downloader wordnet'."
                )
            wordnet.ensure_loaded()
        _WORDNET_READY = True


def possible_lemmas(word: str) -> set[str]:
    """Return the input word and its WordNet lemmas for every supported POS."""
    _ensure_wordnet()
    results = {word}
    normalized_word = word.lower()
    for part_of_speech in _PARTS_OF_SPEECH:
        results.add(_LEMMATIZER.lemmatize(normalized_word, pos=part_of_speech))
    return results
