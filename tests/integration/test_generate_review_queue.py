"""Integration test for scripts/generate_review_queue.py."""

from __future__ import annotations

import importlib.util
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

from src.utilities.tracker import TrackerRow, save_rows


def _import_script(name: str) -> object:
    """Import a script from the ``scripts/`` folder by absolute path."""
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
def test_review_queue_buckets(tmp_path: Path) -> None:
    csv_path = tmp_path / "problem_tracker.csv"
    today = date.today()
    save_rows(
        [
            TrackerRow(
                problem_id="overdue-one",
                source="leetcode",
                difficulty="easy",
                mastery_level=2,
                next_review_date=(today - timedelta(days=3)).isoformat(),
            ),
            TrackerRow(
                problem_id="due-today",
                source="leetcode",
                difficulty="easy",
                mastery_level=3,
                next_review_date=today.isoformat(),
            ),
            TrackerRow(
                problem_id="due-later-this-week",
                source="leetcode",
                difficulty="easy",
                mastery_level=4,
                next_review_date=(today + timedelta(days=4)).isoformat(),
            ),
            TrackerRow(
                problem_id="unscheduled",
                source="leetcode",
                difficulty="easy",
                mastery_level=1,
            ),
            TrackerRow(
                problem_id="retired-should-be-hidden",
                source="leetcode",
                difficulty="easy",
                status="retired",
                mastery_level=5,
                next_review_date=(today - timedelta(days=100)).isoformat(),
            ),
        ],
        csv_path,
    )

    grq = _import_script("generate_review_queue")
    from src.utilities.tracker import load_rows

    rendered = grq._render(load_rows(csv_path), today)  # type: ignore[attr-defined]

    assert "overdue-one" in rendered
    assert "due-today" in rendered
    assert "due-later-this-week" in rendered
    assert "unscheduled" in rendered
    assert "retired-should-be-hidden" not in rendered

    # Bucket counts appear in headings.
    assert "Overdue (1)" in rendered
    assert "Due today (1)" in rendered
    assert "Due this week (1)" in rendered
    assert "Unscheduled (1)" in rendered
