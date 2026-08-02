"""Stack visualization helpers for notebook walkthroughs.

The Min Stack pattern is easiest to understand when the auxiliary stack is
drawn *next to* the main stack at every step, so it is obvious that the two
always have the same height and that the minimum is simply the top of the
second stack.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

# An operation is ("push", value) or ("pop", None).
Operation = tuple[str, int | None]


@dataclass(frozen=True)
class StackState:
    """Both stacks immediately after one operation."""

    label: str
    stack: tuple[int, ...]
    min_stack: tuple[int, ...]

    @property
    def top(self) -> int | None:
        """Top of the main stack, or None when empty."""
        return self.stack[-1] if self.stack else None

    @property
    def minimum(self) -> int | None:
        """Current minimum, read straight off the auxiliary stack."""
        return self.min_stack[-1] if self.min_stack else None


def min_stack_states(operations: Sequence[Operation]) -> list[StackState]:
    """Replay ``operations`` and record both stacks after each one.

    The initial empty state is included first, so the result has
    ``len(operations) + 1`` entries.

    Raises:
        ValueError: On an unknown operation or a pop from an empty stack.
    """
    stack: list[int] = []
    min_stack: list[int] = []
    states = [StackState("init", (), ())]

    for name, value in operations:
        if name == "push":
            if value is None:
                raise ValueError("push requires a value")
            stack.append(value)
            # Mirror the solution: carry the previous minimum forward.
            min_stack.append(value if not min_stack else min(value, min_stack[-1]))
            label = f"push({value})"
        elif name == "pop":
            if not stack:
                raise ValueError("pop from an empty stack")
            stack.pop()
            min_stack.pop()
            label = "pop()"
        else:
            raise ValueError(f"Unknown operation: {name!r}")

        states.append(StackState(label, tuple(stack), tuple(min_stack)))

    return states


def format_min_stack_trace(states: Sequence[StackState]) -> str:
    """Render ``states`` as a plain-text table.

    Dependency-free, so it works in any environment that lacks matplotlib.
    """
    header = ("step", "operation", "stack", "min_stack", "top", "getMin")
    rows = [header]

    for step, state in enumerate(states):
        rows.append(
            (
                str(step),
                state.label,
                "[" + ", ".join(str(v) for v in state.stack) + "]",
                "[" + ", ".join(str(v) for v in state.min_stack) + "]",
                "-" if state.top is None else str(state.top),
                "-" if state.minimum is None else str(state.minimum),
            )
        )

    widths = [max(len(row[col]) for row in rows) for col in range(len(header))]
    lines = ["  ".join(cell.ljust(widths[col]) for col, cell in enumerate(row)) for row in rows]
    # Underline the header so the table reads as a table in plain text.
    lines.insert(1, "  ".join("-" * width for width in widths))
    return "\n".join(lines)


def plot_min_stack_states(
    states: Sequence[StackState],
    *,
    title: str | None = None,
    ax: Any = None,
) -> Any:
    """Draw the main stack and the minimum stack side by side at each step.

    Each step shows two columns of boxes: the main stack on the left and the
    minimum stack on the right. The top box of each column is highlighted,
    because those are the two values ``top()`` and ``getMin()`` return.

    ``matplotlib`` is imported lazily so importing this module stays cheap and
    does not require the dependency.

    Returns the matplotlib ``Axes`` object.
    """
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    if ax is None:
        _, ax = plt.subplots(figsize=(max(6, len(states) * 1.5), 4))

    main_color, min_color = "#4c78a8", "#72b7b2"
    top_main, top_min = "#f58518", "#e45756"
    box_width, gap = 0.38, 0.06

    tallest = max((len(state.stack) for state in states), default=0)

    for step, state in enumerate(states):
        for column, (values, base, top) in enumerate(
            ((state.stack, main_color, top_main), (state.min_stack, min_color, top_min))
        ):
            x = step + column * (box_width + gap) - (box_width + gap) / 2
            for depth, value in enumerate(values):
                # The last box in each column is what the O(1) queries read.
                is_top = depth == len(values) - 1
                ax.add_patch(
                    Rectangle(
                        (x, depth),
                        box_width,
                        0.86,
                        facecolor=top if is_top else base,
                        edgecolor="white",
                    )
                )
                ax.text(
                    x + box_width / 2,
                    depth + 0.43,
                    str(value),
                    ha="center",
                    va="center",
                    color="white",
                    fontsize=9,
                    fontweight="bold" if is_top else "normal",
                )

    ax.set_xticks(range(len(states)))
    ax.set_xticklabels([state.label for state in states], rotation=45, ha="right")
    ax.set_xlim(-0.7, len(states) - 0.3)
    ax.set_ylim(0, max(1, tallest) + 0.3)
    ax.set_yticks(range(max(1, tallest) + 1))
    ax.set_ylabel("depth")
    if title:
        ax.set_title(title)

    # Legend without plotting dummy data points.
    ax.legend(
        handles=[
            Rectangle((0, 0), 1, 1, facecolor=main_color, label="stack"),
            Rectangle((0, 0), 1, 1, facecolor=min_color, label="min_stack"),
            Rectangle((0, 0), 1, 1, facecolor=top_main, label="top() reads this"),
            Rectangle((0, 0), 1, 1, facecolor=top_min, label="getMin() reads this"),
        ],
        loc="upper left",
        fontsize=8,
        framealpha=0.9,
    )
    return ax
