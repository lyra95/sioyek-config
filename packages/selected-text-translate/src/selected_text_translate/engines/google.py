"""Google Translate implementation using its web translation endpoint."""

from __future__ import annotations

import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .base import Translator


class GoogleTranslator(Translator):
    name = "Google Translate"

    def translate(self, source: str) -> str:
        params = urlencode({"client": "gtx", "sl": "auto", "tl": "ko", "dt": "t", "q": source})
        request = Request(
            f"https://translate.googleapis.com/translate_a/single?{params}",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        with urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return "".join(part[0] for part in payload[0] if part and part[0])
