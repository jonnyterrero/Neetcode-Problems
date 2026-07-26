"""Small timing helpers for algorithm comparisons.

Not a replacement for ``pytest-benchmark`` or ``timeit`` for rigorous
measurement — this is a notebook-friendly convenience.
"""

from __future__ import annotations

import statistics
import time
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class BenchmarkResult:
    """Summary of one benchmarked callable."""

    name: str
    mean_seconds: float
    median_seconds: float
    min_seconds: float
    max_seconds: float
    samples: int


def time_function(
    fn: Callable[..., Any],
    *args: Any,
    repeat: int = 5,
    name: str | None = None,
    **kwargs: Any,
) -> BenchmarkResult:
    """Time ``fn(*args, **kwargs)`` ``repeat`` times and summarize."""
    if repeat < 1:
        raise ValueError("repeat must be >= 1")
    timings: list[float] = []
    for _ in range(repeat):
        start = time.perf_counter()
        fn(*args, **kwargs)
        timings.append(time.perf_counter() - start)
    resolved_name: str = name or str(getattr(fn, "__name__", "fn"))
    return BenchmarkResult(
        name=resolved_name,
        mean_seconds=statistics.fmean(timings),
        median_seconds=statistics.median(timings),
        min_seconds=min(timings),
        max_seconds=max(timings),
        samples=repeat,
    )


def compare(
    cases: Iterable[tuple[str, Callable[..., Any], tuple[Any, ...]]],
    *,
    repeat: int = 5,
) -> list[BenchmarkResult]:
    """Time each ``(name, fn, args)`` case and return sorted results."""
    results = [time_function(fn, *args, repeat=repeat, name=name) for name, fn, args in cases]
    return sorted(results, key=lambda r: r.mean_seconds)
