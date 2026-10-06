"""Linked-list visualization helpers for notebook walkthroughs.

The dummy-head merge is easiest to see as three rows: remaining ``list1``,
remaining ``list2``, and the chain growing off the dummy. Each frame is one
pointer rewrite, matching the iterative C++ loop.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Literal

MergeSource = Literal["start", "list1", "list2", "rest1", "rest2", "done"]


@dataclass(frozen=True)
class MergeFrame:
    """One dummy-head merge step.

    ``remaining1`` / ``remaining2`` are the unprocessed prefixes. ``merged`` is
    the real chain after the dummy — dummy itself is never stored, because it
    is not part of the answer.

    ``tail_index`` is the index into ``merged`` that ``tail`` currently points
    at. ``None`` means ``tail`` is still on the dummy. The leftover splice does
    not advance ``tail`` — the C++ returns immediately after hanging the rest
    off ``tail->next``.
    """

    step: int
    remaining1: tuple[int, ...]
    remaining2: tuple[int, ...]
    merged: tuple[int, ...]
    source: MergeSource
    decision: str
    tail_index: int | None


def merge_frames(list1: Sequence[int], list2: Sequence[int]) -> list[MergeFrame]:
    """Replay the iterative two-list merge and record every attach.

    The first frame is the dummy with an empty merged chain. The last frame is
    ``return dummy.next``. In between, each iteration attaches whichever head
    is smaller; after the loop, the leftover list is spliced in a single step,
    including the both-empty case that attaches ``nullptr``.
    """
    remaining1 = list(list1)
    remaining2 = list(list2)
    merged: list[int] = []
    tail_index: int | None = None
    frames = [
        MergeFrame(
            0,
            tuple(remaining1),
            tuple(remaining2),
            (),
            "start",
            "dummy exists; tail sits on dummy",
            tail_index,
        )
    ]

    step = 1
    while remaining1 and remaining2:
        left, right = remaining1[0], remaining2[0]
        if left <= right:
            merged.append(remaining1.pop(0))
            source: MergeSource = "list1"
            decision = f"{left} <= {right}, attach list1"
        else:
            merged.append(remaining2.pop(0))
            source = "list2"
            decision = f"{right} < {left}, attach list2"
        tail_index = len(merged) - 1
        frames.append(
            MergeFrame(
                step,
                tuple(remaining1),
                tuple(remaining2),
                tuple(merged),
                source,
                decision,
                tail_index,
            )
        )
        step += 1

    # Same branch as the C++: leftover list1, otherwise leftover list2
    # (which may itself be empty / nullptr). tail is not advanced.
    if remaining1:
        merged.extend(remaining1)
        remaining1.clear()
        source = "rest1"
        decision = "list2 empty — splice the rest of list1; tail stays put"
    else:
        merged.extend(remaining2)
        remaining2.clear()
        source = "rest2"
        decision = "list1 empty — splice the rest of list2; tail stays put"
    frames.append(
        MergeFrame(
            step,
            tuple(remaining1),
            tuple(remaining2),
            tuple(merged),
            source,
            decision,
            tail_index,
        )
    )
    step += 1
    frames.append(
        MergeFrame(
            step,
            (),
            (),
            tuple(merged),
            "done",
            "return dummy.next — skip the dummy",
            tail_index,
        )
    )
    return frames


def format_merge_trace(frames: Sequence[MergeFrame]) -> str:
    """Render ``frames`` as a plain-text table.

    Dependency-free, so it works in any environment that lacks matplotlib.
    """
    header = ("step", "list1", "list2", "merged", "source", "decision")
    rows: list[tuple[str, ...]] = [header]
    for frame in frames:
        rows.append(
            (
                str(frame.step),
                _fmt_values(frame.remaining1),
                _fmt_values(frame.remaining2),
                _fmt_values(frame.merged),
                frame.source,
                frame.decision,
            )
        )

    widths = [max(len(row[col]) for row in rows) for col in range(len(header))]
    lines = ["  ".join(cell.ljust(widths[col]) for col, cell in enumerate(row)) for row in rows]
    lines.insert(1, "  ".join("-" * width for width in widths))
    return "\n".join(lines)


def plot_merge_frame(frame: MergeFrame, *, ax: Any = None) -> Any:
    """Draw remaining list1, remaining list2, and the dummy-headed merge.

    ``matplotlib`` is imported lazily so importing this module stays cheap and
    does not require the dependency.

    Returns the matplotlib ``Axes`` object.
    """
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

    created = ax is None
    n1 = len(frame.remaining1)
    n2 = len(frame.remaining2)
    n_merged = len(frame.merged)
    # dummy + merged values, or a null sentinel on an empty chain.
    merged_slots = n_merged + 1
    width_nodes = max(n1, n2, merged_slots, 1)

    if created:
        _, ax = plt.subplots(figsize=(max(8.0, width_nodes * 1.55 + 2.4), 6.4))

    ax.set_xlim(-2.4, width_nodes * 1.55 + 1.8)
    ax.set_ylim(-1.4, 6.6)
    ax.axis("off")
    ax.set_title(f"Step {frame.step}   {frame.decision}", loc="left", fontsize=11)

    list1_color = "#4c78a8"
    list2_color = "#72b7b2"
    dummy_color = "#6c757d"
    merged_color = "#2a9d8f"
    just_attached = "#e76f51"

    def _box(x: float, y: float, label: str, face: str, text_color: str = "white") -> None:
        ax.add_patch(
            FancyBboxPatch(
                (x - 0.42, y - 0.32),
                0.84,
                0.64,
                boxstyle="round,pad=0.02,rounding_size=0.08",
                facecolor=face,
                edgecolor="#1d3557",
                linewidth=1.2,
            )
        )
        ax.text(
            x,
            y,
            label,
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
            color=text_color,
        )

    def _arrow(x0: float, x1: float, y: float) -> None:
        ax.add_patch(
            FancyArrowPatch(
                (x0 + 0.46, y),
                (x1 - 0.48, y),
                arrowstyle="-|>",
                mutation_scale=12,
                color="#1d3557",
                linewidth=1.3,
                connectionstyle="arc3,rad=0.0",
            )
        )

    def _chain(
        values: Sequence[int],
        y: float,
        *,
        row_label: str,
        color: str,
        highlight_last: bool = False,
        leading_dummy: bool = False,
    ) -> None:
        ax.text(-1.85, y, row_label, ha="right", va="center", fontsize=10, color="#1d3557")
        xs: list[float] = []
        labels: list[str] = []
        faces: list[str] = []

        if leading_dummy:
            xs.append(0.0)
            labels.append("dum")
            faces.append(dummy_color)

        for offset, value in enumerate(values):
            xs.append((offset + (1 if leading_dummy else 0)) * 1.55)
            labels.append(str(value))
            if (
                highlight_last
                and offset == len(values) - 1
                and frame.source not in {"start", "done"}
            ):
                faces.append(just_attached)
            else:
                faces.append(color if not leading_dummy else merged_color)

        if not xs:
            _box(0.0, y, "null", dummy_color)
            return

        for x, label, face in zip(xs, labels, faces, strict=True):
            text_color = "#1d3557" if face == just_attached else "white"
            _box(x, y, label, face, text_color)

        for left, right in zip(xs, xs[1:], strict=False):
            _arrow(left, right, y)

        null_x = xs[-1] + 1.55
        _box(null_x, y, "null", dummy_color)
        _arrow(xs[-1], null_x, y)

    just_attached_now = frame.source in {"list1", "list2", "rest1", "rest2"}
    _chain(frame.remaining1, 5.0, row_label="list1", color=list1_color)
    _chain(frame.remaining2, 3.15, row_label="list2", color=list2_color)
    _chain(
        frame.merged,
        1.15,
        row_label="merged",
        color=merged_color,
        highlight_last=just_attached_now,
        leading_dummy=True,
    )

    # dummy is at x=0; merged[i] is at (i + 1) * 1.55.
    tail_x = 0.0 if frame.tail_index is None else (frame.tail_index + 1) * 1.55
    ax.annotate(
        "tail",
        xy=(tail_x, 1.50),
        xytext=(tail_x, 2.25),
        ha="center",
        fontsize=10,
        fontweight="bold",
        color="#9b2226",
        arrowprops={"arrowstyle": "->", "color": "#9b2226", "lw": 1.0},
    )

    return ax


def visualize_merge_all(list1: Sequence[int], list2: Sequence[int]) -> None:
    """Print every frame and draw it. Used when ipywidgets is unavailable."""
    import matplotlib.pyplot as plt

    frames = merge_frames(list1, list2)
    print(f"list1={list(list1)}  list2={list(list2)}")
    for frame in frames:
        print(
            f"step {frame.step}: merged={list(frame.merged)}  "
            f"list1={list(frame.remaining1)}  list2={list(frame.remaining2)}  "
            f"{frame.decision}"
        )
        plot_merge_frame(frame)
    plt.show()


def _fmt_values(values: Sequence[int]) -> str:
    return "[" + ", ".join(str(value) for value in values) + "]"
