#!/usr/bin/env python3
"""Update a single row in ``tracking/problem_tracker.csv``."""

from __future__ import annotations

import argparse
import sys
from datetime import date

from _common import ensure_src_on_path

ensure_src_on_path()

from src.utilities.tracker import (  # noqa: E402
    MASTERY_LEVELS,
    VALID_STATUSES,
    next_review_date,
    update_row,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Update mastery, review, and complexity fields on a tracker row.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--problem", required=True, help="problem_id (slug) to update.")
    parser.add_argument("--mastery", type=int, choices=list(MASTERY_LEVELS))
    parser.add_argument("--status", choices=sorted(VALID_STATUSES))
    parser.add_argument("--time", dest="time_complexity", help="Time complexity, e.g. O(n).")
    parser.add_argument("--space", dest="space_complexity", help="Space complexity, e.g. O(1).")
    parser.add_argument("--notes", help="Free-text notes.")
    parser.add_argument(
        "--reviewed",
        action="store_true",
        help="Set last_review_date=today and recompute next_review_date from mastery.",
    )
    parser.add_argument(
        "--attempt",
        action="store_true",
        help="Increment attempt_count by 1.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    updates: dict[str, object] = {}
    if args.mastery is not None:
        updates["mastery_level"] = args.mastery
    if args.status:
        updates["status"] = args.status
        if args.status == "solved":
            updates["solved_date"] = date.today().isoformat()
    if args.time_complexity:
        updates["time_complexity"] = args.time_complexity
    if args.space_complexity:
        updates["space_complexity"] = args.space_complexity
    if args.notes is not None:
        updates["notes"] = args.notes

    if args.reviewed:
        today = date.today()
        updates["last_review_date"] = today.isoformat()
        mastery = args.mastery
        if mastery is None:
            # Look up current mastery to schedule the next review.
            from src.utilities.tracker import load_rows

            for existing in load_rows():
                if existing.problem_id == args.problem:
                    mastery = existing.mastery_level
                    break
        if mastery is None:
            print(
                f"ERROR: No row found for {args.problem!r}; cannot schedule review.",
                file=sys.stderr,
            )
            return 1
        updates["next_review_date"] = next_review_date(mastery, from_date=today).isoformat()

    if args.attempt:
        from src.utilities.tracker import load_rows

        current = next(
            (r for r in load_rows() if r.problem_id == args.problem),
            None,
        )
        if current is None:
            print(f"ERROR: No row found for {args.problem!r}.", file=sys.stderr)
            return 1
        updates["attempt_count"] = current.attempt_count + 1

    if not updates:
        print("Nothing to update. Provide at least one field.", file=sys.stderr)
        return 2

    try:
        row = update_row(args.problem, updates)
    except (KeyError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Updated {row.problem_id!r}: {updates}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
