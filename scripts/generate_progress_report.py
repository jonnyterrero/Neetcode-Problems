#!/usr/bin/env python3
"""Regenerate ``tracking/topic_progress.md`` from the tracker CSV."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

from _common import ensure_src_on_path

ensure_src_on_path()

from src.utilities.paths import repo_root  # noqa: E402
from src.utilities.tracker import TrackerRow, load_rows  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Regenerate the Markdown progress report.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--output", default=None)
    return parser


def _table(counter: Counter[str], header: tuple[str, str]) -> list[str]:
    lines = [
        f"| {header[0]} | {header[1]} |",
        "|---|---|",
    ]
    if not counter:
        lines.append("| _empty_ | 0 |")
        return lines
    for key, value in sorted(counter.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"| {key or '—'} | {value} |")
    return lines


def _render(rows: list[TrackerRow], today: date) -> str:
    total = len(rows)
    by_topic: Counter[str] = Counter(r.topic for r in rows)
    by_difficulty: Counter[str] = Counter(r.difficulty for r in rows)
    by_mastery: Counter[str] = Counter(str(r.mastery_level) for r in rows)
    by_source: Counter[str] = Counter(r.source for r in rows)
    independent = sum(1 for r in rows if r.mastery_level >= 3)  # noqa: PLW0641

    def _is_overdue(r: TrackerRow) -> bool:
        if r.status == "retired" or not r.next_review_date:
            return False
        parsed = _parse(r.next_review_date)
        return parsed is not None and parsed < today

    def _solved_recently(r: TrackerRow) -> bool:
        if not r.solved_date:
            return False
        parsed = _parse(r.solved_date)
        return parsed is not None and today - parsed <= timedelta(days=14)

    overdue = sum(1 for r in rows if _is_overdue(r))
    recent = sum(1 for r in rows if _solved_recently(r))

    strongest = sorted(
        by_topic.items(),
        key=lambda kv: (
            -sum(1 for r in rows if r.topic == kv[0] and r.mastery_level >= 3),
            kv[0],
        ),
    )[:5]
    weakest = sorted(
        by_topic.items(),
        key=lambda kv: (
            sum(1 for r in rows if r.topic == kv[0] and r.mastery_level >= 3) / max(kv[1], 1),
            kv[0],
        ),
    )[:5]

    lines: list[str] = []
    lines.append("# Topic Progress")
    lines.append("")
    lines.append(f"_Generated {today.isoformat()} by `scripts/generate_progress_report.py`._")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total problems: **{total}**")
    lines.append(
        f"- Independent-or-higher (mastery ≥ 3): **{independent}** "
        f"({(100 * independent / total):.1f}%)"
        if total
        else "- Independent-or-higher (mastery ≥ 3): **0**"
    )
    lines.append(f"- Overdue reviews: **{overdue}**")
    lines.append(f"- Solved in the last 14 days: **{recent}**")
    lines.append("")

    lines.append("## By topic")
    lines.extend(_table(by_topic, ("Topic", "Count")))
    lines.append("")

    lines.append("## By difficulty")
    lines.extend(_table(by_difficulty, ("Difficulty", "Count")))
    lines.append("")

    lines.append("## By mastery")
    lines.extend(_table(by_mastery, ("Mastery", "Count")))
    lines.append("")

    lines.append("## By source")
    lines.extend(_table(by_source, ("Source", "Count")))
    lines.append("")

    lines.append("## Most-practiced topics")
    lines.append("")
    lines.append("| Topic | Count |")
    lines.append("|---|---|")
    for topic, count in strongest:
        lines.append(f"| {topic or '—'} | {count} |")
    if not strongest:
        lines.append("| _empty_ | 0 |")
    lines.append("")

    lines.append("## Weakest topics (lowest independent-solve ratio)")
    lines.append("")
    lines.append("| Topic | Count |")
    lines.append("|---|---|")
    for topic, count in weakest:
        lines.append(f"| {topic or '—'} | {count} |")
    if not weakest:
        lines.append("| _empty_ | 0 |")
    lines.append("")

    return "\n".join(lines) + "\n"


def _parse(value: str) -> date | None:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = repo_root()
    output = Path(args.output) if args.output else root / "tracking" / "topic_progress.md"
    rows = load_rows()
    output.write_text(_render(rows, date.today()), encoding="utf-8")
    print(f"Wrote {output.relative_to(root)} ({len(rows)} row(s) considered)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
