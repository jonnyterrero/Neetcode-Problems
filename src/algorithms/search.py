"""Search primitives.

Small, exhaustively tested helpers that make notebook examples clearer
than an inline implementation.
"""

from __future__ import annotations

from collections.abc import Sequence


def binary_search_first(values: Sequence[int], target: int) -> int:
    """Return the leftmost index of ``target`` in a sorted sequence.

    Returns ``-1`` when ``target`` is absent. ``values`` must be sorted in
    non-decreasing order; this precondition is *not* verified for cost
    reasons.

    Time:  O(log n)
    Space: O(1)
    """
    lo, hi = 0, len(values)
    while lo < hi:
        mid = (lo + hi) // 2
        if values[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    if lo < len(values) and values[lo] == target:
        return lo
    return -1
