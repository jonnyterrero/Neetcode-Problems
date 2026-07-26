# Daily Workflow

```
Attempt → Implement → Test → Explain → Track → Review → Commit
```

## 1. Pull

```bash
git pull
```

NeetCode's GitHub Sync may have pushed submissions from the web editor.
Pulling first avoids merge conflicts.

## 2. Attempt

Read the problem. Sketch an approach on paper. Time yourself. Do **not**
look at hints or notebook solutions yet.

## 3. Implement

Scaffold a new problem:

```bash
python scripts/create_problem.py \
  --name "Container With Most Water" \
  --source leetcode --topic two-pointers --difficulty medium
```

This creates `practice/independent/<slug>/solution.py` and appends a
tracker row.

Write the solution. Test it locally:

```bash
python practice/independent/container_with_most_water/solution.py
```

## 4. Test

Write a `test_<slug>.py` next to the solution or inside `tests/unit/`.
Run:

```bash
pytest -k container_with_most_water
```

## 5. Explain

Open (or create) the topic notebook, e.g.
`notebooks/02_two_pointers.ipynb`. Add:

- A one-paragraph restatement in your own words.
- The insight that unlocked the solution.
- Complexity analysis.
- Any mistakes you made.

## 6. Track

Record your mastery:

```bash
python scripts/update_tracker.py \
  --problem "container-with-most-water" \
  --mastery 3 \
  --status solved \
  --time "O(n)" --space "O(1)" \
  --reviewed
```

`--reviewed` sets `last_review_date=today` and recomputes
`next_review_date` from the mastery level.

## 7. Review

Regenerate the review queue whenever you want to see what's due:

```bash
python scripts/generate_review_queue.py
cat tracking/review_queue.md
```

## 8. Commit

```bash
git add .
git commit -m "study: solve container-with-most-water, mastery 3"
git push
```

Use `study:` for practice work; other commit prefixes are listed in
`CONTRIBUTING.md`.

## Weekly

```bash
python scripts/generate_progress_report.py
```

Read `tracking/topic_progress.md` and pick weak topics for next week.
