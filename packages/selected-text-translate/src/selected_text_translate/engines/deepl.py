"""DeepL API Free translation implementation."""

from __future__ import annotations

import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .base import Translator


class DeepLTranslator(Translator):
    name = "DeepL"

    def translate(self, source: str) -> str:
        key = os.environ.get("DEEPL_AUTH_KEY", "").strip()
        if not key:
            raise RuntimeError("Set DEEPL_AUTH_KEY to your DeepL API Free key.")
        body = urlencode({"text": source, "target_lang": "KO"}).encode("utf-8")
        request = Request(
            "https://api-free.deepl.com/v2/translate",
            data=body,
            headers={
                "Authorization": f"DeepL-Auth-Key {key}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        with urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return payload["translations"][0]["text"]
