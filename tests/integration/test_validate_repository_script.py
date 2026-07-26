"""Integration test: `validate_repository.py` on the real repo."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.integration
def test_validate_repository_passes() -> None:
    root = Path(__file__).resolve().parent.parent.parent
    script = root / "scripts" / "validate_repository.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        # Surface the report so failures are actionable.
        pytest.fail(
            f"validate_repository.py failed:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    assert "error(s)" in result.stdout
