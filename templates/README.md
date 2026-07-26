# Templates

Copy from here when starting a new problem. `scripts/create_problem.py` and
`scripts/create_course_problem.py` fill in the placeholders automatically.

| File | Purpose |
|---|---|
| `problem_template.py` | LeetCode-style class + local runner + tests entrypoint. |
| `problem_template.md` | Companion write-up placed next to the solution. |
| `course_problem_template.py` | Coursework problem with numeric-experiment scaffold. |
| `test_template.py` | pytest starter aligned with the solution template. |
| `notebook_template.ipynb` | Structured Jupyter template for topic notes and worked examples. |

Placeholders use double curly braces (e.g. ``{{PROBLEM_NAME}}``) so they
cannot collide with Python or Markdown syntax. The generator scripts do a
plain string replace — no template engine is required.
