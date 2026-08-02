# Working in this repository

This is a personal learning repository for programming fundamentals, CS
coursework, and practice problems. The goal of any change here is **learning
value**, not just a passing submission. Explanations matter as much as code.

## Explanation format for problems

When answering a programming-fundamentals or practice-problem question, use
these sections, in this order:

1. **Setup** — restate the operations/inputs/outputs and the required
   complexity. Name the constraint that makes the naive approach insufficient.
2. **Governing principle** — the single idea the solution rests on.
3. **Algorithm design** — each operation or step, and why it is correct.
4. **Pseudocode** — language-neutral, in a ```text fence.
5. **Python solution** — complete, typed, with docstrings and comments that
   explain *why* rather than restating the code.
6. **Trace the example** — walk the given example step by step, as a table
   with a "why" column where it helps.
7. **Edge-case rationale** — the case that breaks the tempting shortcut.
8. **Complexity analysis** — per-operation table, then space.
9. **Alternative approach** — a second implementation, then an explicit
   recommendation with the reason.

Write every block so it pastes straight into a Jupyter cell:

- Prose and math in markdown cells; code in code cells.
- Math as `$...$` inline and `$$...$$` display. Do not use `\(` or `\[`.
- Pseudocode in ```text fences so it is never mistaken for runnable Python.
- Traces as markdown tables.
- Follow a solution cell with a runnable cell that asserts the example.

## Repository conventions

- **Solutions** — `Data Structures & Algorithms/<problem-slug>/submission-N.py`.
  Keep the platform's exact method names (`getMin`, `isValid`); this directory
  is deliberately excluded from ruff in `pyproject.toml`.
- **Notes** — append to the numbered topic notebook in `notebooks/`
  (e.g. `04_stack.ipynb`), under "Add solved problems below". Structure each
  section on `templates/notebook_template.ipynb`. Never commit cell outputs;
  `scripts/clean_notebook_outputs.py` checks this.
- **Tracker** — add a row to `tracking/problem_tracker.csv` via the
  `src.utilities.tracker` API (`TrackerRow`, `validate_row`, `add_row`,
  `next_review_date`), not by hand-editing the CSV. Then regenerate
  `tracking/topic_progress.md` and `tracking/review_queue.md` with
  `scripts/generate_progress_report.py` and `scripts/generate_review_queue.py`.
  Update mastery later with `scripts/update_tracker.py --problem <slug>`.
- **Reusable helpers** — `src/algorithms/` for algorithms,
  `src/visualizations/` for notebook plotting. Import matplotlib *lazily*
  inside functions so the package stays importable without it. Export new
  helpers in the package `__init__.py` and add tests under `tests/unit/`.
- **Scaffolding new practice work** — `scripts/create_problem.py` writes into
  `practice/`. Do not run it for a problem already solved under
  `Data Structures & Algorithms/`; it would duplicate the scaffolding.

## Before committing

Run all four; they are fast:

```bash
make lint          # ruff check .
make format-check  # ruff format --check .
make test          # pytest
make validate      # scripts/validate_repository.py
```

Notebooks *are* linted. When a notebook cell holds a platform signature like
`getMin`, that is covered by the `notebooks/**/*.ipynb` per-file-ignore in
`pyproject.toml` — extend that rule rather than scattering `# noqa`.

Dev dependencies are not always installed in a fresh environment; run
`pip install -e ".[dev]"` first if a tool is missing.
