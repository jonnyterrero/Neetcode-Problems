"""Shared library for the learning system.

Sub-packages:

- :mod:`src.algorithms` — reusable, well-tested algorithm primitives.
- :mod:`src.visualizations` — small plotting helpers for notebooks.
- :mod:`src.benchmarking` — timing and complexity-comparison utilities.
- :mod:`src.utilities` — filesystem, slug, and tracker helpers used by
  the automation scripts and tests.
"""

__all__ = ["algorithms", "visualizations", "benchmarking", "utilities"]
