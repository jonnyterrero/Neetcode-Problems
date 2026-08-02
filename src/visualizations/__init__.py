"""Notebook plotting helpers.

Import ``matplotlib`` lazily so tests that do not exercise visualization
do not require the dependency to be installed.
"""

from src.visualizations.arrays import plot_array_bars
from src.visualizations.stacks import (
    StackState,
    format_min_stack_trace,
    min_stack_states,
    plot_min_stack_states,
)

__all__ = [
    "StackState",
    "format_min_stack_trace",
    "min_stack_states",
    "plot_array_bars",
    "plot_min_stack_states",
]
