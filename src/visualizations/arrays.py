"""Array bar-chart helpers for notebook walkthroughs."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any


def plot_array_bars(
    values: Sequence[int],
    *,
    highlight: Sequence[int] | None = None,
    title: str | None = None,
    ax: Any = None,
) -> Any:
    """Render ``values`` as a bar chart, optionally highlighting indices.

    ``matplotlib`` is imported lazily so importing this module is cheap and
    does not require the dependency.

    Returns the matplotlib ``Axes`` object.
    """
    # Import inside the function so ``pip install -e .`` works without
    # matplotlib for anyone who only needs the CLI scripts.
    import matplotlib.pyplot as plt

    if ax is None:
        _, ax = plt.subplots(figsize=(max(4, len(values) * 0.4), 3))

    xs = list(range(len(values)))
    colors = ["#4c78a8"] * len(values)
    for idx in highlight or []:
        if 0 <= idx < len(values):
            colors[idx] = "#f58518"

    ax.bar(xs, values, color=colors)
    ax.set_xticks(xs)
    if title:
        ax.set_title(title)
    ax.set_ylabel("value")
    ax.set_xlabel("index")
    return ax
