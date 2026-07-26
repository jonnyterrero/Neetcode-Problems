# Practice

Manual, hand-written practice that lives outside NeetCode's sync.

| Subdirectory | Purpose |
|---|---|
| `independent/` | Solved from scratch without hints. |
| `timed/` | Attempts made under a time limit (e.g. mock interviews). |
| `reattempts/` | Second and later passes at problems already tracked. |
| `failed_attempts/` | Attempts you could not finish. Keep them — they are the highest-signal review material. |
| `pattern_drills/` | Short drills targeting a specific pattern (e.g. sliding window rehearsal). |

## How to add a problem

```bash
python scripts/create_problem.py \
  --name "Container With Most Water" \
  --source leetcode --topic two-pointers --difficulty medium \
  --category independent
```

By default the script creates:

```
practice/<category>/<slug>/
    solution.py
    NOTES.md
```

and appends a row to `tracking/problem_tracker.csv`.

## About the example problem

`practice/independent/count-consecutive-runs/` is an **original** example
included to demonstrate the system end-to-end. Delete it once you have
your own work. See its `NOTES.md`.
