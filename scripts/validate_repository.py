#!/usr/bin/env python3
"""Check repository invariants — schema, notebooks, and structure."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from _common import ensure_src_on_path

ensure_src_on_path()

from src.utilities.paths import repo_root  # noqa: E402
from src.utilities.tracker import (  # noqa: E402
    MASTERY_LEVELS,
    TRACKER_COLUMNS,
    VALID_DIFFICULTIES,
    VALID_SOURCES,
    VALID_STATUSES,
    load_rows,
    tracker_path,
)

REQUIRED_FILES = (
    "README.md",
    "LICENSE",
    "pyproject.toml",
    ".gitignore",
    "tracking/problem_tracker.csv",
    "templates/problem_template.py",
    "templates/notebook_template.ipynb",
    "docs/setup.md",
    "docs/workflow.md",
)

REQUIRED_DIRS = (
    "notebooks",
    "practice",
    "coursework",
    "src",
    "tests",
    "tracking",
    "templates",
    "scripts",
    "docs",
    ".github/workflows",
)

# Notebook output cells over this size (bytes) are flagged as bloated.
MAX_OUTPUT_BYTES = 200_000

# Suspicious file patterns that indicate accidental commits.
SECRET_LIKE = (
    ".env",
    "id_rsa",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    "credentials.json",
    "aws-credentials",
)

# Substrings in filenames that suggest restricted coursework content.
RESTRICTED_COURSEWORK_HINTS = (
    "answer_key",
    "answer-key",
    "solutions-key",
    "solutions_key",
    "exam-",
    "midterm-",
    "final-exam",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate the repository layout, tracker, and notebooks.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--notebooks-only",
        action="store_true",
        help="Only run notebook checks.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures (exit non-zero).",
    )
    return parser


class Report:
    """Accumulator for validation messages."""

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.passes: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def ok(self, message: str) -> None:
        self.passes.append(message)

    def print(self) -> None:
        for msg in self.passes:
            print(f"  ok    {msg}")
        for msg in self.warnings:
            print(f"  warn  {msg}")
        for msg in self.errors:
            print(f"  FAIL  {msg}")


def check_required_layout(root: Path, report: Report) -> None:
    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            report.error(f"missing required file: {rel}")
        else:
            report.ok(f"present: {rel}")
    for rel in REQUIRED_DIRS:
        if not (root / rel).is_dir():
            report.error(f"missing required directory: {rel}")


def check_tracker(root: Path, report: Report) -> None:
    csv_path = tracker_path(root)
    if not csv_path.exists():
        report.error("tracker CSV missing")
        return
    header = csv_path.read_text(encoding="utf-8").splitlines()[0].split(",")
    expected = list(TRACKER_COLUMNS)
    if header != expected:
        report.error(
            "tracker header does not match schema:\n"
            f"    expected: {expected}\n    got:      {header}"
        )
        return
    report.ok("tracker header matches schema")

    seen: set[str] = set()
    for row in load_rows(csv_path):
        if row.problem_id in seen:
            report.error(f"duplicate problem_id: {row.problem_id}")
        seen.add(row.problem_id)

        if row.mastery_level not in MASTERY_LEVELS:
            report.error(f"{row.problem_id}: invalid mastery_level {row.mastery_level}")
        if row.status not in VALID_STATUSES:
            report.error(f"{row.problem_id}: invalid status {row.status!r}")
        if row.difficulty not in VALID_DIFFICULTIES:
            report.error(f"{row.problem_id}: invalid difficulty {row.difficulty!r}")
        if row.source not in VALID_SOURCES:
            report.error(f"{row.problem_id}: invalid source {row.source!r}")

        for date_field in (
            "first_attempt_date",
            "solved_date",
            "last_review_date",
            "next_review_date",
        ):
            value = getattr(row, date_field)
            if value and not _is_iso_date(value):
                report.error(f"{row.problem_id}: {date_field} not YYYY-MM-DD ({value!r})")

        if row.solution_path and not (root / row.solution_path).exists():
            report.warn(f"{row.problem_id}: solution_path does not exist ({row.solution_path})")
        if row.notebook_path and not (root / row.notebook_path).exists():
            report.warn(f"{row.problem_id}: notebook_path does not exist ({row.notebook_path})")
    report.ok(f"tracker rows validated: {len(seen)}")


def _is_iso_date(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def _iter_notebooks(root: Path):
    for ipynb in root.rglob("*.ipynb"):
        parts = set(ipynb.parts)
        if ".ipynb_checkpoints" in parts or ".venv" in parts:
            continue
        yield ipynb


def check_notebooks(root: Path, report: Report) -> None:
    count = 0
    for ipynb in _iter_notebooks(root):
        count += 1
        rel = ipynb.relative_to(root)
        try:
            data = json.loads(ipynb.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            report.error(f"{rel}: invalid notebook JSON ({exc})")
            continue

        if not isinstance(data, dict) or "cells" not in data:
            report.error(f"{rel}: notebook missing 'cells'")
            continue

        cells = data.get("cells") or []
        total_output_bytes = 0
        for idx, cell in enumerate(cells):
            outputs = cell.get("outputs") or []
            for out in outputs:
                if out.get("output_type") == "error":
                    report.warn(f"{rel}: cell {idx} has an error traceback committed")
                total_output_bytes += len(json.dumps(out, ensure_ascii=False))
        if total_output_bytes > MAX_OUTPUT_BYTES:
            report.warn(
                f"{rel}: total notebook output size {total_output_bytes} B "
                f"exceeds {MAX_OUTPUT_BYTES} B"
            )

        if "metadata" not in data or not data["metadata"]:
            report.warn(f"{rel}: no notebook metadata")
    report.ok(f"notebooks validated: {count}")


def check_suspicious_files(root: Path, report: Report) -> None:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        parts = set(path.parts)
        if ".git" in parts or ".venv" in parts or "node_modules" in parts:
            continue
        rel = path.relative_to(root)
        name_lower = path.name.lower()
        rel_lower = str(rel).lower()

        for pattern in SECRET_LIKE:
            if pattern in name_lower:
                report.error(f"possible secret file committed: {rel}")

        if rel_lower.startswith("coursework/"):
            for hint in RESTRICTED_COURSEWORK_HINTS:
                if hint in name_lower:
                    report.warn(f"restricted-looking coursework file: {rel} (hint: {hint!r})")
    report.ok("suspicious-file scan complete")


def check_venv_not_committed(root: Path, report: Report) -> None:
    """Fail only if a venv directory is present AND not ignored by .gitignore.

    A local venv is expected during development. Only committed venvs are
    a problem — approximated here by checking whether the directory name
    appears in ``.gitignore``.
    """
    gitignore = root / ".gitignore"
    ignored = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    for candidate in (".venv", "venv", "env"):
        target = root / candidate
        if not target.is_dir():
            continue
        if f"{candidate}/" in ignored or f"{candidate}\n" in ignored:
            continue
        report.error(f"virtual environment present and not gitignored: {candidate}/")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = repo_root()
    report = Report()

    if args.notebooks_only:
        check_notebooks(root, report)
    else:
        check_required_layout(root, report)
        check_tracker(root, report)
        check_notebooks(root, report)
        check_venv_not_committed(root, report)
        check_suspicious_files(root, report)

    report.print()
    print("")
    print(
        f"summary: {len(report.passes)} passed, "
        f"{len(report.warnings)} warning(s), {len(report.errors)} error(s)"
    )
    if report.errors or (args.strict and report.warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
