"""Notebook plotting helpers.

Import ``matplotlib`` lazily so tests that do not exercise visualization
do not require the dependency to be installed.
"""

from src.visualizations.arrays import plot_array_bars
from src.visualizations.linked_lists import (
    MergeFrame,
    format_merge_trace,
    merge_frames,
    plot_merge_frame,
    visualize_merge_all,
)
from src.visualizations.stacks import (
    StackState,
    format_min_stack_trace,
    min_stack_states,
    plot_min_stack_states,
)

__all__ = [
    "MergeFrame",
    "StackState",
    "format_merge_trace",
    "format_min_stack_trace",
    "merge_frames",
    "min_stack_states",
    "plot_array_bars",
    "plot_merge_frame",
    "plot_min_stack_states",
    "visualize_merge_all",
]
