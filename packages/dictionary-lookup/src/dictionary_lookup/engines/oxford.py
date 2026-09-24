"""Oxford Learner's Dictionary search engine."""

from __future__ import annotations

from html.parser import HTMLParser
import re
from urllib.parse import quote
from urllib.request import Request, urlopen

from .base import DictionaryEngine


class _DefinitionsParser(HTMLParser):
    VOID_TAGS = {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr",
    }

    def __init__(self) -> None:
        super().__init__()
        self.depth = 0
        self.parts: list[str] = []
        self.entries: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = dict(attrs).get("class", "").split()
        if self.depth:
            if tag not in self.VOID_TAGS:
                self.depth += 1
        elif tag == "span" and "def" in classes:
            self.depth = 1
            self.parts = []
        if self.depth and tag in {"br", "li", "p"}:
            self.parts.append(" ")

    def handle_endtag(self, tag: str) -> None:
        if self.depth and tag not in self.VOID_TAGS:
            self.depth -= 1
            if self.depth == 0:
                definition = re.sub(r"\s+", " ", "".join(self.parts)).strip()
                if definition:
                    self.entries.append(definition)

    def handle_data(self, data: str) -> None:
        if self.depth:
            self.parts.append(data)


class OxfordLearnersDictionary(DictionaryEngine):
    name = "Oxford"
    window_title = "Oxford lookup"

    def lookup(self, word: str) -> list[str]:
        url_word = quote(word.lower().replace(" ", "-"), safe="'-")
        url = f"https://www.oxfordlearnersdictionaries.com/definition/english/{url_word}"
        request = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; SioyekOxfordLookup/1.0)"})
        with urlopen(request, timeout=12) as response:
            page = response.read().decode("utf-8", "replace")
        parser = _DefinitionsParser()
        parser.feed(page)
        return parser.entries[:30]
