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
  needed.
- Cons: costs credits after the free monthly allowance.

To use, click **Code → Codespaces** on GitHub. The container clones
this repo automatically; run `pip install -e ".[dev]"` inside it.

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
