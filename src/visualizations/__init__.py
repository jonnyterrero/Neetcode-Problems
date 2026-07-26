"""Notebook plotting helpers.

Import ``matplotlib`` lazily so tests that do not exercise visualization
do not require the dependency to be installed.
"""

from src.visualizations.arrays import plot_array_bars

__all__ = ["plot_array_bars"]
