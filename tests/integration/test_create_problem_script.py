"""Integration test for scripts/create_problem.py.

The script writes into the real repo when run via its CLI. To keep tests
isolated we exercise its ``main`` function against a temporary tracker CSV
by monkeypatching :func:`tracker_path`.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

import pytest


def _import_script(name: str) -> object:
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
def test_create_problem_scaffold(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Build a minimal repo skeleton so the script can find its templates.
    repo_root = tmp_path / "repo"
    (repo_root / "templates").mkdir(parents=True)
    (repo_root / "practice" / "independent").mkdir(parents=True)
    (repo_root / "tracking").mkdir(parents=True)
    (repo_root / "pyproject.toml").write_text("", encoding="utf-8")

    # Copy real templates so the substitution logic is exercised end-to-end.
    real_root = Path(__file__).resolve().parent.parent.parent
    for name in ("problem_template.py", "problem_template.md"):
        (repo_root / "templates" / name).write_text(
            (real_root / "templates" / name).read_text(encoding="utf-8"),
            encoding="utf-8",
        )

    # Empty tracker.
    tracker_csv = repo_root / "tracking" / "problem_tracker.csv"
    from src.utilities.tracker import TRACKER_COLUMNS

    tracker_csv.write_text(",".join(TRACKER_COLUMNS) + "\n", encoding="utf-8")

    # Point repo_root() and tracker_path() at our fake repo.
    monkeypatch.setattr("src.utilities.paths.repo_root", lambda start=None: repo_root)
    monkeypatch.setattr("src.utilities.tracker.tracker_path", lambda root=None: tracker_csv)

    cp = _import_script("create_problem")
    # Re-import the tracker to force lookups through the patched functions.
    monkeypatch.setattr(cp, "repo_root", lambda start=None: repo_root)

    # Chdir into repo_root to be safe.
    os.chdir(repo_root)

    exit_code = cp.main(  # type: ignore[attr-defined]
        [
            "--name",
            "Sample Problem",
            "--source",
            "leetcode",
            "--topic",
            "two-pointers",
            "--difficulty",
            "easy",
            "--url",
            "https://example.com/sample",
        ]
    )
    assert exit_code == 0

    solution = repo_root / "practice" / "independent" / "sample_problem" / "solution.py"
    notes = repo_root / "practice" / "independent" / "sample_problem" / "NOTES.md"
    assert solution.exists()
    assert notes.exists()

    solution_text = solution.read_text(encoding="utf-8")
    assert "Sample Problem" in solution_text
    assert "leetcode" in solution_text

    # Tracker should now include the row.
    tracker_lines = tracker_csv.read_text(encoding="utf-8").splitlines()
    assert any(line.startswith("sample-problem,") for line in tracker_lines)
