"""{{PROBLEM_NAME}}.

Course:            {{COURSE}}
Unit:              {{UNIT}}
Source:            course
Topic:             {{TOPIC}}
Difficulty:        n/a
Time complexity:   O(?)
Space complexity:  O(?)
Mastery level:     0
Last review:       {{TODAY}}
Next review:       {{NEXT_REVIEW}}

Coursework note
---------------
Do not commit graded exam questions, restricted solution keys, or
copyrighted assignment PDFs. Restate the problem in your own words and
store your original implementation only. See docs/coursework_privacy.md.
"""

from __future__ import annotations

from collections.abc import Callable


def solve(x: float) -> float:
    """Replace with the real numeric routine."""
    raise NotImplementedError


def experiment(
    fn: Callable[[float], float] = solve,
    *,
    inputs: list[float] | None = None,
) -> list[tuple[float, float]]:
    """Run the routine over a set of inputs and return ``(x, y)`` pairs."""
    xs = inputs if inputs is not None else [0.0, 0.5, 1.0]
    return [(x, fn(x)) for x in xs]


def main() -> None:
    for x, y in experiment():
        print(f"x={x:>6.3f}  y={y:>10.6f}")


if __name__ == "__main__":
    main()
