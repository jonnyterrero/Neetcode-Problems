"""{{PROBLEM_NAME}}.

Source:            {{SOURCE}}
URL:               {{PROBLEM_URL}}
Topic:             {{TOPIC}}
Difficulty:        {{DIFFICULTY}}
Time complexity:   O(?)
Space complexity:  O(?)
Mastery level:     0
Last review:       {{TODAY}}
Next review:       {{NEXT_REVIEW}}
"""

from __future__ import annotations

from collections.abc import Sequence


class Solution:
    """LeetCode-style class. Keep the method signature the platform expects."""

    def solve(self, values: Sequence[int]) -> int:
        """Replace this with the real signature and body.

        Args:
            values: Input placeholder.

        Returns:
            Result placeholder.
        """
        raise NotImplementedError


# Local, hand-written examples. Add before writing the solution to make the
# expected behavior concrete. Prefer *original* examples over copy-pasted
# problem statements.
EXAMPLES: list[tuple[tuple, object]] = [
    # ((args,), expected),
    # ((([1, 2, 3],)), 6),
]


def run_examples() -> None:
    """Run the local examples and assert equality. Prints on success."""
    solution = Solution()
    for args, expected in EXAMPLES:
        result = solution.solve(*args)
        assert result == expected, f"solve{args} -> {result!r}, expected {expected!r}"
    print(f"OK: {len(EXAMPLES)} example(s) passed for {{PROBLEM_NAME}}")


if __name__ == "__main__":
    run_examples()
