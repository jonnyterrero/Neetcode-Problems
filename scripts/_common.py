"""Shared helpers for scripts. Adds ``src`` to ``sys.path`` when needed."""

from __future__ import annotations

import sys
from pathlib import Path


def ensure_src_on_path() -> Path:
    """Insert the repository root onto ``sys.path`` if it is missing.

    This lets ``python scripts/foo.py`` work without ``pip install -e .``
    for anyone who just cloned the repo.
    """
    here = Path(__file__).resolve().parent.parent
    if str(here) not in sys.path:
        sys.path.insert(0, str(here))
    return here
