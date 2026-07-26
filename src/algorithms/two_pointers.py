"""Two-pointer primitives used by notebooks and tests."""

from __future__ import annotations

from collections.abc import Sequence


def max_container_area(heights: Sequence[int]) -> int:
    """Return the maximum water area between two vertical lines.

    Classic two-pointer sweep. Not a submission — used by the notebook
    walkthrough and tests as an *original* implementation that mirrors the
    pattern without copying any external problem statement.
    """
    if len(heights) < 2:
        return 0
    left, right = 0, len(heights) - 1
    best = 0
    while left < right:
        area = (right - left) * min(heights[left], heights[right])
        if area > best:
            best = area
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    return best


def valid_palindrome_alphanumeric(text: str) -> bool:
    """Return True if ``text`` reads the same forwards and backwards.

    Ignores non-alphanumeric characters and is case-insensitive. Uses two
    pointers to avoid allocating a filtered copy.
    """
    left, right = 0, len(text) - 1
    while left < right:
        while left < right and not text[left].isalnum():
            left += 1
        while left < right and not text[right].isalnum():
            right -= 1
        if text[left].lower() != text[right].lower():
            return False
        left += 1
        right -= 1
    return True
