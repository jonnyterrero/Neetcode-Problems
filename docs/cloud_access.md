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

1. On the repo page: **Code → Codespaces → Create codespace on main**.
2. Wait for the container to build (first time only, ~1–2 min).
3. In the Codespace terminal:

   ```bash
   pip install -e ".[dev]"
   ```

4. Open any notebook from `notebooks/`.
5. When prompted, pick the Python kernel (the container already has
   `ipykernel` installed as a dev dep).
6. Edit → save → commit → push. A Codespace is a real git checkout, so
   the standard git workflow works unchanged:

   ```bash
   git pull --rebase
   git add . && git commit -m "study: …"
   git push
   ```

7. **Stop the Codespace** from the GitHub Codespaces page when done —
   idle Codespaces still consume free-tier hours until they auto-suspend.

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
