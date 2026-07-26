# Tests

Runs via `pytest`. Split into:

- `unit/` — no filesystem side effects outside `tmp_path`.
- `integration/` — exercise multi-step behavior (e.g. create a problem,
  then update the tracker, then generate a review queue) inside
  `tmp_path`.

Run everything:

```bash
pytest
```

Fast subset:

```bash
pytest -m unit
```

Coverage:

```bash
pytest --cov --cov-report=term-missing
```

Tests never touch the real `tracking/problem_tracker.csv`. They point the
tracker helpers at a temporary CSV via the `path=` keyword argument.
