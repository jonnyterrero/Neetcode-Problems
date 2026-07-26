# Setup

Full local setup, tested on Python 3.11 and 3.12.

## 1. Prerequisites

- Python 3.11 or newer (`python --version`)
- Git
- Optional: `make` (macOS/Linux comes with it; Windows users can install
  it via `choco install make` or just run the Python commands directly)

## 2. Clone

```bash
git clone https://github.com/jonnyterrero/Neetcode-Problems.git
cd Neetcode-Problems
```

## 3. Create and activate a virtual environment

**macOS / Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell refuses to run the activation script, allow scripts for
the current session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Windows (cmd):**

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

## 4. Install dev dependencies

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

`-e .` installs `src` in editable mode so `from src.utilities import ...`
resolves consistently for scripts, tests, and notebooks.

## 5. Verify

```bash
pytest
ruff check .
ruff format --check .
python scripts/validate_repository.py
```

All four should exit `0`.

## 6. Launch JupyterLab (optional)

```bash
jupyter lab
```

Navigate to `notebooks/` in the file browser and open any topic notebook.

## 7. VS Code

1. Install the **Python** and **Jupyter** extensions.
2. Open the repo folder.
3. `Ctrl+Shift+P` → **Python: Select Interpreter** → choose
   `.venv/bin/python` (or `.venv\Scripts\python.exe` on Windows).
4. Open any notebook; VS Code will prompt to install `ipykernel` if
   missing (already in dev deps).
5. Choose the matching kernel when prompted.

## Makefile equivalents

Windows users without `make` can run the Python commands directly.

| `make` target | Python equivalent |
|---|---|
| `make setup` | `pip install -e ".[dev]"` |
| `make test` | `pytest` |
| `make lint` | `ruff check .` |
| `make format` | `ruff format .` |
| `make format-check` | `ruff format --check .` |
| `make typecheck` | `mypy scripts src` |
| `make validate` | `python scripts/validate_repository.py` |
| `make notebooks` | `python scripts/validate_repository.py --notebooks-only` |
| `make review` | `python scripts/generate_review_queue.py` |
| `make report` | `python scripts/generate_progress_report.py` |
| `make clean-notebooks` | `python scripts/clean_notebook_outputs.py --apply` |

## Troubleshooting

- **`ModuleNotFoundError: src`** — you skipped `pip install -e .`.
  Reinstall dev deps.
- **Kernel is missing in VS Code / Jupyter** — activate the venv, then
  `python -m ipykernel install --user --name neetcode-problems`.
- **Ruff reports issues in synced files** — you should not be linting
  `Data Structures & Algorithms/`. Confirm `pyproject.toml` still lists
  it under `extend-exclude`.
