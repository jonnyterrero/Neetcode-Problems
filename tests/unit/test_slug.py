"""Tests for :func:`src.utilities.slug.slugify`."""

from __future__ import annotations

import pytest

from src.utilities.slug import slugify


@pytest.mark.unit
@pytest.mark.parametrize(
    "raw, expected",
    [
        ("Container With Most Water", "container-with-most-water"),
        ("Two Sum II — Sorted Input!", "two-sum-ii-sorted-input"),
        ("  Multiple   Spaces  ", "multiple-spaces"),
        ("already-a-slug", "already-a-slug"),
        ("MiXeD_case_123", "mixed-case-123"),
        ("café-society", "cafe-society"),
    ],
)
def test_slugify_produces_expected(raw: str, expected: str) -> None:
    assert slugify(raw) == expected


@pytest.mark.unit
@pytest.mark.parametrize("raw", ["", "   ", "!!!", "---"])
def test_slugify_empty_when_no_alphanumeric(raw: str) -> None:
    assert slugify(raw) == ""


@pytest.mark.unit
def test_slugify_rejects_non_string() -> None:
    with pytest.raises(TypeError):
        slugify(123)  # type: ignore[arg-type]
