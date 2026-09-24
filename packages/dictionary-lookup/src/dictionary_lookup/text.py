"""Text normalization helpers for dictionary lookups."""


def trim(text: str) -> str:
    """Remove leading and trailing characters that are not letters or digits."""
    start = 0
    end = len(text)
    while start < end and not text[start].isalnum():
        start += 1
    while end > start and not text[end - 1].isalnum():
        end -= 1
    return text[start:end]
