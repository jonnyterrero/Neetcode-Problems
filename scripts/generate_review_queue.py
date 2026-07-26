#!/usr/bin/env python3
"""Regenerate ``tracking/review_queue.md`` from the tracker CSV."""

from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta
from pathlib import Path

from _common import ensure_src_on_path

ensure_src_on_path()

from src.utilities.paths import repo_root  # noqa: E402
from src.utilities.tracker import TrackerRow, load_rows  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Regenerate the Markdown review queue.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Override output path (defaults to tracking/review_queue.md).",
    )
    return parser


def _parse(value: str) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def _bucket(rows: list[TrackerRow], today: date) -> dict[str, list[TrackerRow]]:
    week = today + timedelta(days=7)
    buckets: dict[str, list[TrackerRow]] = {
        "overdue": [],
        "today": [],
        "this_week": [],
        "unscheduled": [],
        "below_mastery_3": [],
    }
    for row in rows:
        if row.status == "retired":
            continue
        review = _parse(row.next_review_date)
        if review is None:
            buckets["unscheduled"].append(row)
        elif review < today:
            buckets["overdue"].append(row)
        elif review == today:
            buckets["today"].append(row)
        elif review <= week:
            buckets["this_week"].append(row)
        if row.mastery_level < 3:
            buckets["below_mastery_3"].append(row)
    return buckets


def _render(rows: list[TrackerRow], today: date) -> str:
    buckets = _bucket(rows, today)
    lines: list[str] = []
    lines.append("# Review Queue")
    lines.append("")
    lines.append(f"_Generated {today.isoformat()} by `scripts/generate_review_queue.py`._")
    lines.append("")
    total = sum(1 for r in rows if r.status != "retired")
    lines.append(f"Total tracked problems (excluding retired): **{total}**")
    lines.append("")

    section_titles = {
        "overdue": "Overdue",
        "today": "Due today",
        "this_week": "Due this week",
        "unscheduled": "Unscheduled",
        "below_mastery_3": "Below mastery level 3",
    }
    for key, title in section_titles.items():
        section_rows = buckets[key]
        lines.append(f"## {title} ({len(section_rows)})")
        if not section_rows:
            lines.append("")
            lines.append("_None._")
            lines.append("")
            continue
        lines.append("")
        lines.append("| Problem | Topic | Mastery | Next review | Solution |")
        lines.append("|---|---|---|---|---|")
        for row in sorted(section_rows, key=lambda r: (r.next_review_date, r.problem_id)):
            lines.append(
                f"| `{row.problem_id}` | {row.topic or '—'} | {row.mastery_level} "
                f"| {row.next_review_date or '—'} | {row.solution_path or '—'} |"
            )
        lines.append("")

    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = repo_root()
    output = Path(args.output) if args.output else root / "tracking" / "review_queue.md"
    rows = load_rows()
    output.write_text(_render(rows, date.today()), encoding="utf-8")
    print(f"Wrote {output.relative_to(root)} ({len(rows)} row(s) considered)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
