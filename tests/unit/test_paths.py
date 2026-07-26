"""Tests for :func:`src.utilities.paths.repo_root`."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.utilities.paths import repo_root


@pytest.mark.unit
def test_repo_root_finds_actual_repo() -> None:
    root = repo_root()
    assert (root / "pyproject.toml").exists()
    assert (root / "tracking").is_dir()


@pytest.mark.unit
def test_repo_root_from_synthetic_tree(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("", encoding="utf-8")
    nested = tmp_path / "a" / "b" / "c"
    nested.mkdir(parents=True)
    assert repo_root(nested) == tmp_path


@pytest.mark.unit
def test_repo_root_raises_when_missing(tmp_path: Path) -> None:
    # Skip if the actual filesystem root happens to contain markers.
    if any((Path("/") / marker).exists() for marker in ("pyproject.toml", ".git")):
        pytest.skip("filesystem root has repo markers")
    nested = tmp_path / "isolated"
    nested.mkdir()
    with pytest.raises(RuntimeError):
        repo_root(nested)
