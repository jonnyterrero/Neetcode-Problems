"""Repository-root discovery.

Scripts and tests should never assume the current working directory. Use
:func:`repo_root` to resolve paths relative to the repository root.
"""

from __future__ import annotations

from pathlib import Path


def repo_root(start: Path | None = None) -> Path:
    """Return the repository root by walking up from ``start``.

    A directory is considered the repository root when it contains any of
    ``pyproject.toml``, ``.git``, or ``tracking/problem_tracker.csv``.

    Args:
        start: Directory to start searching from. Defaults to this file's
            parent so behavior is independent of the caller's CWD.

    Returns:
        Absolute path of the discovered root.

    Raises:
        RuntimeError: If no root is found before reaching the filesystem root.
    """
    here = (start or Path(__file__).resolve().parent).resolve()
    markers = ("pyproject.toml", ".git", "tracking")
    for candidate in [here, *here.parents]:
        if any((candidate / marker).exists() for marker in markers):
            return candidate
    raise RuntimeError(f"Could not locate repository root from {here}")
