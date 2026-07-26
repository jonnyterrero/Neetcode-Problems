"""Integration test for scripts/generate_progress_report.py."""

from __future__ import annotations

import importlib.util
import sys
from datetime import date
from pathlib import Path

import pytest

from src.utilities.tracker import TrackerRow


def _import_script(name: str) -> object:
    root = Path(__file__).resolve().parent.parent.parent
    scripts_dir = root / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    spec = importlib.util.spec_from_file_location(name, scripts_dir / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.integration
def test_progress_report_counts() -> None:
    gpr = _import_script("generate_progress_report")
    rows = [
        TrackerRow(
            problem_id="a",
            source="leetcode",
            topic="arrays-and-hashing",
            difficulty="easy",
            mastery_level=4,
            status="solved",
            solved_date=date.today().isoformat(),
        ),
        TrackerRow(
            problem_id="b",
            source="neetcode",
            topic="two-pointers",
            difficulty="medium",
            mastery_level=2,
            status="in-progress",
        ),
        TrackerRow(
            problem_id="c",
            source="course",
            topic="numerical-methods",
            difficulty="n/a",
            mastery_level=5,
        ),
    ]
    rendered = gpr._render(rows, date.today())  # type: ignore[attr-defined]
    assert "Total problems: **3**" in rendered
    assert "arrays-and-hashing" in rendered
    assert "two-pointers" in rendered
    assert "numerical-methods" in rendered
    assert "leetcode" in rendered
    assert "neetcode" in rendered
    assert "course" in rendered
