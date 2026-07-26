"""Tests for :mod:`src.algorithms`."""

from __future__ import annotations

import pytest

from src.algorithms import (
    binary_search_first,
    max_container_area,
    valid_palindrome_alphanumeric,
)


@pytest.mark.unit
@pytest.mark.parametrize(
    "values, target, expected",
    [
        ([], 3, -1),
        ([3], 3, 0),
        ([1, 2, 3, 4, 5], 3, 2),
        ([1, 2, 2, 2, 3], 2, 1),  # leftmost
        ([1, 2, 3], 4, -1),
        ([1, 2, 3], 0, -1),
    ],
)
def test_binary_search_first(values: list[int], target: int, expected: int) -> None:
    assert binary_search_first(values, target) == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "heights, expected",
    [
        ([], 0),
        ([5], 0),
        ([1, 1], 1),
        ([1, 8, 6, 2, 5, 4, 8, 3, 7], 49),
        ([4, 3, 2, 1, 4], 16),
    ],
)
def test_max_container_area(heights: list[int], expected: int) -> None:
    assert max_container_area(heights) == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "text, expected",
    [
        ("", True),
        ("a", True),
        ("A man, a plan, a canal: Panama", True),
        ("race a car", False),
        (".,", True),  # no alnum characters
        ("No 'x' in Nixon", True),
    ],
)
def test_valid_palindrome(text: str, expected: bool) -> None:
    assert valid_palindrome_alphanumeric(text) is expected
