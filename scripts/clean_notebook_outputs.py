#!/usr/bin/env python3
"""Safely strip outputs from tracked notebooks.

Dry-run by default. Requires ``--apply`` to write changes. Use before
committing large notebook outputs.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from _common import ensure_src_on_path

ensure_src_on_path()

from src.utilities.paths import repo_root  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Strip outputs and execution_count from notebooks.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Notebook paths (default: every tracked .ipynb).",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write changes. Without this flag, only prints what would change.",
    )
    return parser


def _iter_targets(root: Path, paths: list[str]) -> list[Path]:
    if paths:
        return [Path(p).resolve() for p in paths]
    result: list[Path] = []
    for ipynb in root.rglob("*.ipynb"):
        parts = set(ipynb.parts)
        if ".ipynb_checkpoints" in parts or ".venv" in parts:
            continue
        result.append(ipynb)
    return result


def _clean(data: dict) -> tuple[dict, bool]:
    changed = False
    for cell in data.get("cells", []):
        if cell.get("cell_type") == "code":
            if cell.get("outputs"):
                cell["outputs"] = []
                changed = True
            if cell.get("execution_count") is not None:
                cell["execution_count"] = None
                changed = True
    return data, changed


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = repo_root()
    targets = _iter_targets(root, args.paths)

    modified = 0
    for path in targets:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"SKIP  {path}: {exc}")
            continue
        cleaned, changed = _clean(data)
        if not changed:
            continue
        modified += 1
        if args.apply:
            path.write_text(
                json.dumps(cleaned, indent=1, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            print(f"CLEAN {path.relative_to(root)}")
        else:
            print(f"WOULD {path.relative_to(root)}")

    print("")
    if args.apply:
        print(f"Cleaned {modified} notebook(s).")
    else:
        print(f"Dry run: {modified} notebook(s) would be cleaned. Re-run with --apply.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
