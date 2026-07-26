"""Slug generation for problem folders and tracker IDs."""

from __future__ import annotations

import re
import unicodedata

_ALLOWED = re.compile(r"[^a-z0-9]+")


def slugify(value: str) -> str:
    """Convert an arbitrary string to a filesystem- and URL-safe slug.

    - Lowercases.
    - Strips accents.
    - Replaces any run of disallowed characters with a single ``-``.
    - Trims leading and trailing ``-``.

    >>> slugify("Container With Most Water")
    'container-with-most-water'
    >>> slugify("Two Sum II — Sorted Input!")
    'two-sum-ii-sorted-input'
    >>> slugify("   ")
    ''
    """
    if not isinstance(value, str):
        raise TypeError(f"slugify expected str, got {type(value).__name__}")
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    lowered = normalized.lower()
    cleaned = _ALLOWED.sub("-", lowered).strip("-")
    return cleaned
