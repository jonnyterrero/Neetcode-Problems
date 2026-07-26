"""Tests for the original example problem shipped with the repo."""

from __future__ import annotations

import pytest

from practice.independent.count_consecutive_runs.solution import (
    EXAMPLES,
    Solution,
)


@pytest.mark.unit
def test_examples_all_pass() -> None:
    solution = Solution()
    for args, expected in EXAMPLES:
        assert solution.count_runs(*args) == expected


@pytest.mark.unit
def test_generator_input() -> None:
    # count_runs iterates once; a generator should still work.
    solution = Solution()
    assert solution.count_runs(iter([1, 1, 2, 2, 3])) == 3


@pytest.mark.unit
def test_string_input() -> None:
    # Strings are iterable sequences of characters — should count runs.
    solution = Solution()
    assert solution.count_runs("aaabbc") == 3
