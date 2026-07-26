"""Read, write, and mutate ``tracking/problem_tracker.csv``.

The CSV is the source of truth for mastery and review scheduling. All
mutations funnel through the helpers here so behavior stays consistent
across scripts and tests.
"""

from __future__ import annotations

import csv
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path

from src.utilities.paths import repo_root

TRACKER_COLUMNS: tuple[str, ...] = (
    "problem_id",
    "problem_name",
    "source",
    "problem_url",
    "topic",
    "subtopic",
    "difficulty",
    "language",
    "status",
    "mastery_level",
    "first_attempt_date",
    "solved_date",
    "last_review_date",
    "next_review_date",
    "attempt_count",
    "time_complexity",
    "space_complexity",
    "solution_path",
    "notebook_path",
    "notes",
)

MASTERY_LEVELS: tuple[int, ...] = (0, 1, 2, 3, 4, 5)

# Days until next review, keyed by mastery level. Kept small and explicit.
REVIEW_INTERVAL_DAYS: dict[int, int] = {
    0: 1,
    1: 1,
    2: 3,
    3: 7,
    4: 21,
    5: 45,
}

VALID_STATUSES: frozenset[str] = frozenset({"unsolved", "in-progress", "solved", "retired"})
VALID_SOURCES: frozenset[str] = frozenset({"neetcode", "leetcode", "course", "book", "other"})
VALID_DIFFICULTIES: frozenset[str] = frozenset({"easy", "medium", "hard", "n/a"})


@dataclass
class TrackerRow:
    """Typed view of a tracker row.

    Only ``problem_id`` is required; other fields default to sensible empty
    values. Use :meth:`to_csv_dict` for CSV serialization.
    """

    problem_id: str
    problem_name: str = ""
    source: str = "other"
    problem_url: str = ""
    topic: str = ""
    subtopic: str = ""
    difficulty: str = "n/a"
    language: str = "python"
    status: str = "unsolved"
    mastery_level: int = 0
    first_attempt_date: str = ""
    solved_date: str = ""
    last_review_date: str = ""
    next_review_date: str = ""
    attempt_count: int = 0
    time_complexity: str = ""
    space_complexity: str = ""
    solution_path: str = ""
    notebook_path: str = ""
    notes: str = ""
    extras: dict[str, str] = field(default_factory=dict, repr=False)

    def to_csv_dict(self) -> dict[str, str]:
        """Return a stringified dict suitable for :class:`csv.DictWriter`."""
        return {
            "problem_id": self.problem_id,
            "problem_name": self.problem_name,
            "source": self.source,
            "problem_url": self.problem_url,
            "topic": self.topic,
            "subtopic": self.subtopic,
            "difficulty": self.difficulty,
            "language": self.language,
            "status": self.status,
            "mastery_level": str(self.mastery_level),
            "first_attempt_date": self.first_attempt_date,
            "solved_date": self.solved_date,
            "last_review_date": self.last_review_date,
            "next_review_date": self.next_review_date,
            "attempt_count": str(self.attempt_count),
            "time_complexity": self.time_complexity,
            "space_complexity": self.space_complexity,
            "solution_path": self.solution_path,
            "notebook_path": self.notebook_path,
            "notes": self.notes,
        }


def tracker_path(root: Path | None = None) -> Path:
    """Return the absolute path of the tracker CSV."""
    return (root or repo_root()) / "tracking" / "problem_tracker.csv"


def _coerce_int(value: str, *, default: int = 0) -> int:
    value = (value or "").strip()
    if not value:
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"Expected integer, got {value!r}") from exc


def load_rows(path: Path | None = None) -> list[TrackerRow]:
    """Load all rows from the tracker CSV.

    Missing files are treated as empty; missing columns default to empty.
    """
    csv_path = path or tracker_path()
    if not csv_path.exists():
        return []
    with csv_path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        rows: list[TrackerRow] = []
        for raw in reader:
            row = TrackerRow(
                problem_id=(raw.get("problem_id") or "").strip(),
                problem_name=(raw.get("problem_name") or "").strip(),
                source=(raw.get("source") or "other").strip() or "other",
                problem_url=(raw.get("problem_url") or "").strip(),
                topic=(raw.get("topic") or "").strip(),
                subtopic=(raw.get("subtopic") or "").strip(),
                difficulty=(raw.get("difficulty") or "n/a").strip() or "n/a",
                language=(raw.get("language") or "python").strip() or "python",
                status=(raw.get("status") or "unsolved").strip() or "unsolved",
                mastery_level=_coerce_int(raw.get("mastery_level", "0")),
                first_attempt_date=(raw.get("first_attempt_date") or "").strip(),
                solved_date=(raw.get("solved_date") or "").strip(),
                last_review_date=(raw.get("last_review_date") or "").strip(),
                next_review_date=(raw.get("next_review_date") or "").strip(),
                attempt_count=_coerce_int(raw.get("attempt_count", "0")),
                time_complexity=(raw.get("time_complexity") or "").strip(),
                space_complexity=(raw.get("space_complexity") or "").strip(),
                solution_path=(raw.get("solution_path") or "").strip(),
                notebook_path=(raw.get("notebook_path") or "").strip(),
                notes=(raw.get("notes") or "").strip(),
            )
            if not row.problem_id:
                # Skip blank lines rather than crash.
                continue
            rows.append(row)
    return rows


def save_rows(rows: Iterable[TrackerRow], path: Path | None = None) -> None:
    """Write ``rows`` to the tracker CSV, replacing existing content."""
    csv_path = path or tracker_path()
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(TRACKER_COLUMNS))
        writer.writeheader()
        for row in rows:
            writer.writerow(row.to_csv_dict())


def add_row(row: TrackerRow, path: Path | None = None) -> None:
    """Append ``row``, refusing to insert a duplicate ``problem_id``."""
    validate_row(row)
    rows = load_rows(path)
    if any(existing.problem_id == row.problem_id for existing in rows):
        raise ValueError(f"Duplicate problem_id: {row.problem_id!r}")
    rows.append(row)
    save_rows(rows, path)


def update_row(
    problem_id: str,
    updates: dict[str, object],
    *,
    path: Path | None = None,
) -> TrackerRow:
    """Apply ``updates`` to the row with matching ``problem_id``.

    Returns the updated row. Raises ``KeyError`` if no row matches.
    """
    rows = load_rows(path)
    for index, row in enumerate(rows):
        if row.problem_id == problem_id:
            for key, value in updates.items():
                if not hasattr(row, key):
                    raise ValueError(f"Unknown tracker field: {key!r}")
                setattr(row, key, value)
            validate_row(row)
            rows[index] = row
            save_rows(rows, path)
            return row
    raise KeyError(f"No tracker row with problem_id={problem_id!r}")


def validate_row(row: TrackerRow) -> None:
    """Raise ``ValueError`` if ``row`` violates the schema."""
    if not row.problem_id:
        raise ValueError("problem_id is required")
    if row.source not in VALID_SOURCES:
        raise ValueError(f"Invalid source {row.source!r}; expected one of {sorted(VALID_SOURCES)}")
    if row.difficulty not in VALID_DIFFICULTIES:
        raise ValueError(
            f"Invalid difficulty {row.difficulty!r}; expected one of {sorted(VALID_DIFFICULTIES)}"
        )
    if row.status not in VALID_STATUSES:
        raise ValueError(f"Invalid status {row.status!r}; expected one of {sorted(VALID_STATUSES)}")
    if row.mastery_level not in MASTERY_LEVELS:
        raise ValueError(
            f"Invalid mastery_level {row.mastery_level!r}; expected one of {list(MASTERY_LEVELS)}"
        )
    if row.attempt_count < 0:
        raise ValueError("attempt_count must be >= 0")
    for date_field in (
        "first_attempt_date",
        "solved_date",
        "last_review_date",
        "next_review_date",
    ):
        value = getattr(row, date_field)
        if value and not _is_iso_date(value):
            raise ValueError(f"{date_field} must be YYYY-MM-DD, got {value!r}")


def _is_iso_date(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def next_review_date(
    mastery_level: int,
    *,
    from_date: date | None = None,
    intervals: dict[int, int] | None = None,
) -> date:
    """Return the next review date for a given mastery level.

    ``intervals`` can override the defaults if a caller wants a different
    schedule. Unknown mastery levels raise ``ValueError``.
    """
    schedule = intervals or REVIEW_INTERVAL_DAYS
    if mastery_level not in schedule:
        raise ValueError(f"No interval configured for mastery_level={mastery_level!r}")
    base = from_date or date.today()
    return base + timedelta(days=schedule[mastery_level])
