#!/usr/bin/env python3
"""Create a new independent practice problem folder and tracker row."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from _common import ensure_src_on_path

ensure_src_on_path()

from src.utilities.paths import repo_root  # noqa: E402
from src.utilities.slug import slugify  # noqa: E402
from src.utilities.tracker import (  # noqa: E402
    TrackerRow,
    add_row,
    next_review_date,
)

VALID_CATEGORIES = ("independent", "timed", "reattempts", "failed_attempts", "pattern_drills")
VALID_SOURCES = ("leetcode", "neetcode", "book", "other")
VALID_DIFFICULTIES = ("easy", "medium", "hard")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scaffold a manual practice problem.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--name", required=True, help="Problem title, in plain English.")
    parser.add_argument("--source", required=True, choices=VALID_SOURCES)
    parser.add_argument("--topic", required=True, help="e.g. two-pointers")
    parser.add_argument("--difficulty", required=True, choices=VALID_DIFFICULTIES)
    parser.add_argument("--language", default="python", help="Solution language.")
    parser.add_argument("--url", default="", help="Problem URL (optional).")
    parser.add_argument("--category", default="independent", choices=VALID_CATEGORIES)
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files (defaults to refuse).",
    )
    return parser


def _copy_template(
    template_path: Path,
    destination: Path,
    replacements: dict[str, str],
    *,
    force: bool,
) -> None:
    if destination.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite {destination}. Use --force to override.")
    text = template_path.read_text(encoding="utf-8")
    for key, value in replacements.items():
        text = text.replace(f"{{{{{key}}}}}", value)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    slug = slugify(args.name)
    if not slug:
        print("ERROR: --name must contain at least one alphanumeric character.", file=sys.stderr)
        return 2

    root = repo_root()
    today = date.today().isoformat()
    next_review = next_review_date(0).isoformat()
    replacements = {
        "PROBLEM_NAME": args.name,
        "SLUG": slug,
        "SOURCE": args.source,
        "TOPIC": args.topic,
        "DIFFICULTY": args.difficulty,
        "PROBLEM_URL": args.url,
        "TODAY": today,
        "NEXT_REVIEW": next_review,
    }

    problem_dir = root / "practice" / args.category / slug.replace("-", "_")
    solution_path = problem_dir / "solution.py"
    notes_path = problem_dir / "NOTES.md"

    try:
        _copy_template(
            root / "templates" / "problem_template.py",
            solution_path,
            replacements,
            force=args.force,
        )
        _copy_template(
            root / "templates" / "problem_template.md",
            notes_path,
            replacements,
            force=args.force,
        )
    except FileExistsError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    solution_rel = solution_path.relative_to(root).as_posix()
    row = TrackerRow(
        problem_id=slug,
        problem_name=args.name,
        source=args.source,
        problem_url=args.url,
        topic=args.topic,
        difficulty=args.difficulty,
        language=args.language,
        status="in-progress",
        mastery_level=0,
        first_attempt_date=today,
        next_review_date=next_review,
        attempt_count=1,
        solution_path=solution_rel,
    )

    try:
        add_row(row)
    except ValueError as exc:
        print(f"WARNING: tracker not updated: {exc}", file=sys.stderr)
        # Still consider the scaffold a success — the user can fix the tracker.
        return 0

    print(f"Created  {solution_path.relative_to(root)}")
    print(f"Created  {notes_path.relative_to(root)}")
    print(f"Tracker  appended row {slug!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
