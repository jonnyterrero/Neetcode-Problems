# Cloud Access

Three different capabilities. Do not confuse them.

## Cloud storage vs. cloud execution

- **Storage.** GitHub is the permanent, canonical home for this
  repository. Every commit is durable.
- **Execution.** Notebook cells need a Python environment. That
  environment can live on your laptop, in Codespaces, or in Colab.
- **Local execution.** VS Code or JupyterLab against your `.venv` is
  the default and most reliable option.

## Recommended: local execution

- Fastest.
- Free.
- No dependency on any third-party notebook service.
- Full access to the `src/` package via `pip install -e .`.

Setup is in `docs/setup.md`.

## GitHub Codespaces (optional)

A full VS Code environment in the cloud, backed by a container built
from your repo.

- Pros: identical to local, works on Chromebooks or tablets, no laptop
  needed. Free-tier ≈ 60 hours/month per user.
- Cons: costs credits after the free monthly allowance.

### Step-by-step

This repository ships a `.devcontainer/devcontainer.json` so a fresh
Codespace comes fully configured — no manual `pip install`, no manual
extension setup, no interpreter picking.

1. On the repo page: **Code → Codespaces → Create codespace on main**.
2. Wait for the container to build (~2–3 minutes the first time).
   During the build, the devcontainer:
   - starts from `mcr.microsoft.com/devcontainers/python:1-3.12`;
   - runs `pip install -e '.[dev]'`;
   - installs the Python, Pylance, Jupyter, and Ruff VS Code extensions;
   - selects `/usr/local/bin/python` as the interpreter;
   - turns on pytest, format-on-save with Ruff, and Ruff auto-fixes on
     save.
3. When the editor opens, open any notebook from `notebooks/` and pick
   the offered **Python 3.12** kernel.
4. Confirm the environment works from the Codespace terminal:

   ```bash
   pytest -q
   python scripts/validate_repository.py
   ```

5. Edit → save → commit → push. A Codespace is a real git checkout, so
   the standard git workflow works unchanged:

   ```bash
   git pull --rebase
   git add . && git commit -m "study: …"
   git push
   ```

6. **Stop the Codespace** from
   [github.com/codespaces](https://github.com/codespaces) when done —
   idle Codespaces still consume free-tier hours until they auto-suspend
   (default: 30 minutes of inactivity).

### Updating the Codespace config later

If you edit `.devcontainer/devcontainer.json`, run **Codespaces:
Rebuild Container** from the Codespace's command palette to pick up
changes. Existing work is preserved across the rebuild.

## Google Colab (optional)

Colab can open any `.ipynb` in the repo:

```
https://colab.research.google.com/github/jonnyterrero/Neetcode-Problems/blob/main/notebooks/01_arrays_and_hashing.ipynb
```

- Pros: zero setup, GPU/TPU on demand.
- Cons:
  - The `src/` package is not installed — `from src.algorithms import ...`
    will fail unless you `git clone` the repo inside the Colab session
    first.
  - Changes made in Colab are **not** committed to GitHub automatically.
    You must download the notebook and push it manually, or use Colab's
    GitHub integration (File → Save a copy in GitHub).

## Rules for cloud execution

- Never paste secrets into a hosted notebook cell.
- Never rely on Colab or Codespaces for persistent state. GitHub is the
  only durable store.
- Never let a hosted environment write to your tracker CSV via a
  drive-mounted path — commit through git only.

## Related

- LeetCode auto-sync setup: [`leetcode_sync.md`](leetcode_sync.md).
- Multi-device / pull-rebase discipline:
  [`workflow.md`](workflow.md#multi-device-and-neetcode-sync-safety).
