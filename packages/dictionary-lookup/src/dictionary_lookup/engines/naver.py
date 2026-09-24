"""Naver English Dictionary search engine."""

from __future__ import annotations

from html.parser import HTMLParser
import json
import re
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .base import DictionaryEngine


class _TextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"br", "p", "li"}:
            self.parts.append(" ")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def _plain_text(value: object) -> str:
    if not isinstance(value, str):
        return ""
    parser = _TextParser()
    parser.feed(value)
    return re.sub(r"\s+", " ", "".join(parser.parts)).strip()


class NaverEnglishDictionary(DictionaryEngine):
    name = "Naver"
    window_title = "Naver lookup"
    search_url = "https://en.dict.naver.com/api3/enko/search"

    def lookup(self, word: str) -> list[str]:
        query = urlencode({"query": word, "m": "pc"})
        request = Request(
            f"{self.search_url}?{query}",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
                "Referer": "https://en.dict.naver.com/",
                "Accept": "application/json, text/plain, */*",
            },
        )
        with urlopen(request, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8", "replace"))

        try:
            items = payload["searchResultMap"]["searchResultListMap"]["WORD"]["items"]
        except (KeyError, TypeError):
            return []

        definitions: list[str] = []
        for item in items:
            if not isinstance(item, dict):
                continue
            headword = _plain_text(item.get("handleEntry") or item.get("expEntry"))
            for group in item.get("meansCollector", []):
                if not isinstance(group, dict):
                    continue
                part_of_speech = _plain_text(group.get("partOfSpeech"))
                for meaning in group.get("means", []):
                    if not isinstance(meaning, dict):
                        continue
                    definition = _plain_text(meaning.get("value"))
                    if not definition:
                        continue
                    label = f"{headword}: " if headword else ""
                    if part_of_speech:
                        label += f"[{part_of_speech}] "
                    definitions.append(label + definition)

        return definitions[:30]
