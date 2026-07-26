"""Count consecutive runs — an ORIGINAL example problem.

This is not from LeetCode or NeetCode. It exists purely to show the
end-to-end shape of a practice problem in this repository. Delete or
adapt freely.

Problem
-------
Given a sequence of integers, return the number of *runs* — maximal
consecutive subsequences of equal values.

Examples
    []                     -> 0
    [7]                    -> 1
    [1, 1, 2, 2, 2, 1, 1]  -> 3
    [1, 2, 1, 2, 1]        -> 5

Source:            original (this repository)
Topic:             arrays-and-hashing
Difficulty:        easy
Time complexity:   O(n)
Space complexity:  O(1)
Mastery level:     3
Last review:       2026-07-26
Next review:       2026-08-02
"""

from __future__ import annotations

from collections.abc import Sequence


class Solution:
    """Solver for the count-consecutive-runs problem."""

    def count_runs(self, values: Sequence[int]) -> int:
        """Return the number of maximal runs of equal values.

        Args:
            values: Any indexable sequence of comparable elements.

        Returns:
            The count of runs. Empty input returns 0.
        """
        runs = 0
        previous: object = object()  # sentinel guaranteed to be unequal
        for value in values:
            if value != previous:
                runs += 1
                previous = value
        return runs


EXAMPLES: list[tuple[tuple[Sequence[int], ...], int]] = [
    (([],), 0),
    (([7],), 1),
    (([1, 1, 2, 2, 2, 1, 1],), 3),
    (([1, 2, 1, 2, 1],), 5),
    (([5, 5, 5, 5],), 1),
]


def run_examples() -> None:
    """Assert every example produces the expected result."""
    solution = Solution()
    for args, expected in EXAMPLES:
        result = solution.count_runs(*args)
        assert result == expected, f"count_runs{args} -> {result}, expected {expected}"
    print(f"OK: {len(EXAMPLES)} example(s) passed for count-consecutive-runs")


if __name__ == "__main__":
    run_examples()
