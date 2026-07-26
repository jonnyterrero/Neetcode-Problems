# Notebook Guide

## Philosophy

Notebooks are for **learning**, not for shipping. Use them to:

- Explain concepts.
- Visualize algorithms.
- Compare approaches side-by-side.
- Record what you tried and why it failed.
- Benchmark implementations.
- Connect algorithmic patterns to coursework and engineering.

Clean `.py` files remain the source of truth for tested, runnable code.

## Layout

- `notebooks/01_..` through `notebooks/18_..` — one notebook per major
  NeetCode topic. See `notebooks/README.md`.
- Per-problem notebooks (optional) go in the same folder as the topic
  they belong to, prefixed with the topic number:
  `notebooks/02b_two_pointers_container_with_most_water.ipynb`.

## Template

Copy `templates/notebook_template.ipynb` for a per-problem write-up.
Sections align with the problem template so notes migrate easily.

## Kernel

Always run against the `.venv` kernel (see `docs/setup.md`). If VS Code
shows a stale kernel:

1. `Ctrl+Shift+P` → **Jupyter: Select Interpreter to Start Jupyter Server**
2. Pick the venv interpreter.
3. Reload window.

## What NOT to put in notebooks

- Full copies of external problem statements (copyright).
- Datasets over ~200 KB.
- Model weights.
- Local paths, personal identifiers, API keys.
- Long tracebacks — clean them out before committing.

## Cleaning outputs before commit

Dry-run:

```bash
python scripts/clean_notebook_outputs.py
```

Apply:

```bash
python scripts/clean_notebook_outputs.py --apply
```

You can also target a single file:

```bash
python scripts/clean_notebook_outputs.py --apply notebooks/07_trees.ipynb
```

## Diff quality (optional)

Third-party tools like [`nbdime`](https://nbdime.readthedocs.io) and
[`nbstripout`](https://github.com/kynan/nbstripout) improve notebook
diffing. They are not required — the built-in
`scripts/clean_notebook_outputs.py` covers the common case.

## Validating notebooks

Fast structural check (runs in CI):

```bash
python scripts/validate_repository.py --notebooks-only
```

This checks JSON validity, warns about committed error tracebacks, and
flags oversized outputs. It does **not** execute cells — coursework
notebooks can require unavailable data.
