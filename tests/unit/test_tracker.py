"""Tests for :mod:`src.utilities.tracker`."""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import pytest

from src.utilities.tracker import (
    REVIEW_INTERVAL_DAYS,
    TRACKER_COLUMNS,
    TrackerRow,
    add_row,
    load_rows,
    next_review_date,
    save_rows,
    update_row,
    validate_row,
)


@pytest.fixture
def tracker_csv(tmp_path: Path) -> Path:
    return tmp_path / "problem_tracker.csv"


@pytest.mark.unit
def test_columns_are_stable() -> None:
    # Guard: the schema is part of the public contract.
    assert TRACKER_COLUMNS[0] == "problem_id"
    assert TRACKER_COLUMNS[-1] == "notes"
    assert len(TRACKER_COLUMNS) == 20


@pytest.mark.unit
def test_next_review_date_uses_interval_table() -> None:
    for level, delta in REVIEW_INTERVAL_DAYS.items():
        result = next_review_date(level, from_date=date(2026, 7, 26))
        assert result == date(2026, 7, 26) + timedelta(days=delta)


@pytest.mark.unit
def test_next_review_date_rejects_unknown_level() -> None:
    with pytest.raises(ValueError):
        next_review_date(99)


@pytest.mark.unit
def test_validate_row_ok() -> None:
    row = TrackerRow(problem_id="foo", source="leetcode", difficulty="easy")
    validate_row(row)  # should not raise


@pytest.mark.unit
@pytest.mark.parametrize(
    "mutation",
    [
        {"problem_id": ""},
        {"source": "instagram"},
        {"difficulty": "unknown"},
        {"status": "half-solved"},
        {"mastery_level": 7},
        {"attempt_count": -1},
        {"first_attempt_date": "2026/07/26"},
    ],
)
def test_validate_row_rejects_bad_fields(mutation: dict) -> None:
    row = TrackerRow(problem_id="foo", source="leetcode", difficulty="easy")
    for key, value in mutation.items():
        setattr(row, key, value)
    with pytest.raises(ValueError):
        validate_row(row)


@pytest.mark.unit
def test_add_and_load_roundtrip(tracker_csv: Path) -> None:
    row = TrackerRow(
        problem_id="example",
        problem_name="Example",
        source="leetcode",
        topic="arrays",
        difficulty="easy",
        mastery_level=2,
    )
    save_rows([], tracker_csv)
    add_row(row, tracker_csv)
    loaded = load_rows(tracker_csv)
    assert len(loaded) == 1
    assert loaded[0].problem_id == "example"
    assert loaded[0].mastery_level == 2


@pytest.mark.unit
def test_add_row_rejects_duplicate(tracker_csv: Path) -> None:
    row = TrackerRow(problem_id="dup", source="leetcode", difficulty="easy")
    save_rows([], tracker_csv)
    add_row(row, tracker_csv)
    with pytest.raises(ValueError):
        add_row(row, tracker_csv)


@pytest.mark.unit
def test_update_row_applies_and_persists(tracker_csv: Path) -> None:
    row = TrackerRow(
        problem_id="p1",
        source="leetcode",
        difficulty="medium",
        mastery_level=0,
    )
    save_rows([row], tracker_csv)
    update_row("p1", {"mastery_level": 3, "status": "solved"}, path=tracker_csv)
    reloaded = load_rows(tracker_csv)[0]
    assert reloaded.mastery_level == 3
    assert reloaded.status == "solved"


@pytest.mark.unit
def test_update_row_unknown_id(tracker_csv: Path) -> None:
    save_rows([], tracker_csv)
    with pytest.raises(KeyError):
        update_row("nope", {"mastery_level": 1}, path=tracker_csv)


@pytest.mark.unit
def test_update_row_rejects_unknown_field(tracker_csv: Path) -> None:
    row = TrackerRow(problem_id="p1", source="leetcode", difficulty="easy")
    save_rows([row], tracker_csv)
    with pytest.raises(ValueError):
        update_row("p1", {"not_a_field": 1}, path=tracker_csv)


@pytest.mark.unit
def test_load_ignores_blank_problem_id(tracker_csv: Path) -> None:
    save_rows(
        [
            TrackerRow(problem_id="a", source="leetcode", difficulty="easy"),
        ],
        tracker_csv,
    )
    # Append a blank line manually.
    with tracker_csv.open("a", encoding="utf-8") as fh:
        fh.write("," * (len(TRACKER_COLUMNS) - 1) + "\n")
    loaded = load_rows(tracker_csv)
    assert [r.problem_id for r in loaded] == ["a"]
