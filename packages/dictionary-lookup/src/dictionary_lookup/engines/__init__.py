"""Dictionary search engine implementations."""

from .base import DictionaryEngine
from .naver import NaverEnglishDictionary
from .oxford import OxfordLearnersDictionary

ENGINES: dict[str, DictionaryEngine] = {
    engine.name: engine for engine in (OxfordLearnersDictionary(), NaverEnglishDictionary())
}

__all__ = ["DictionaryEngine", "ENGINES"]
