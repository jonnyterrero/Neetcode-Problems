#!/usr/bin/env python3
"""Create a new coursework practice problem."""

from __future__ import annotations

import argparse
import sys
from datetime import date

from _common import ensure_src_on_path

ensure_src_on_path()

from src.utilities.paths import repo_root  # noqa: E402
from src.utilities.slug import slugify  # noqa: E402
from src.utilities.tracker import (  # noqa: E402
    TrackerRow,
    add_row,
    next_review_date,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scaffold a coursework practice problem.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--course", required=True, help="Course slug or folder name.")
    parser.add_argument("--unit", required=True, help="Unit or topic within the course.")
    parser.add_argument("--name", required=True, help="Problem title, in plain English.")
    parser.add_argument("--topic", default="", help="Optional cross-topic tag.")
    parser.add_argument("--language", default="python")
    parser.add_argument("--force", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    slug = slugify(args.name)
    if not slug:
        print("ERROR: --name must contain at least one alphanumeric character.", file=sys.stderr)
        return 2

    course_slug = slugify(args.course).replace("-", "_") or args.course
    unit_slug = slugify(args.unit).replace("-", "_") or args.unit
    root = repo_root()
    today = date.today().isoformat()
    next_review = next_review_date(0).isoformat()

    problem_dir = root / "coursework" / course_slug / unit_slug / slug.replace("-", "_")
    solution_path = problem_dir / "solution.py"
    notes_path = problem_dir / "NOTES.md"

    if not args.force and (solution_path.exists() or notes_path.exists()):
        print(f"ERROR: Refusing to overwrite files in {problem_dir}. Use --force.", file=sys.stderr)
        return 1

    replacements = {
        "PROBLEM_NAME": args.name,
        "SLUG": slug,
        "COURSE": args.course,
        "UNIT": args.unit,
        "TOPIC": args.topic or args.unit,
        "TODAY": today,
        "NEXT_REVIEW": next_review,
    }

    template_py = (root / "templates" / "course_problem_template.py").read_text(encoding="utf-8")
    template_md = (root / "templates" / "problem_template.md").read_text(encoding="utf-8")
    for key, value in replacements.items():
        template_py = template_py.replace(f"{{{{{key}}}}}", value)
        template_md = template_md.replace(f"{{{{{key}}}}}", value)

    problem_dir.mkdir(parents=True, exist_ok=True)
    solution_path.write_text(template_py, encoding="utf-8")
    notes_path.write_text(template_md, encoding="utf-8")

    solution_rel = solution_path.relative_to(root).as_posix()
    row = TrackerRow(
        problem_id=f"course-{course_slug}-{slug}",
        problem_name=args.name,
        source="course",
        topic=args.topic or args.unit,
        subtopic=args.unit,
        difficulty="n/a",
        language=args.language,
        status="in-progress",
        mastery_level=0,
        first_attempt_date=today,
        next_review_date=next_review,
        attempt_count=1,
        solution_path=solution_rel,
        notes=f"course={args.course}; unit={args.unit}",
    )

    try:
        add_row(row)
    except ValueError as exc:
        print(f"WARNING: tracker not updated: {exc}", file=sys.stderr)
        return 0

    print(f"Created  {solution_path.relative_to(root)}")
    print(f"Created  {notes_path.relative_to(root)}")
    print(f"Tracker  appended row {row.problem_id!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
