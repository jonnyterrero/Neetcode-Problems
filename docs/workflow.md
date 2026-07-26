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

## Multi-device and NeetCode-sync safety

NeetCode's GitHub Sync also pushes to `main` — from the web editor,
often while you are working locally. If your local `main` is behind
when you try to push, git rejects with "non-fast-forward". Adopt this
discipline to avoid divergent history:

```bash
# Start of every session on any machine:
git pull --rebase

# ... work ...

# Right before every push:
git pull --rebase
git push
```

`--rebase` replays your local commits on top of whatever landed
remotely, so history stays linear. If you forget and get a
"non-fast-forward" error, the fix is the same:

```bash
git pull --rebase
# resolve conflicts if any (rare — NeetCode and your notes touch
# different folders); then:
git rebase --continue
git push
```

### Verifying your notebook changes reach GitHub

Sanity check to run once end-to-end:

```bash
# 1. Edit and save a notebook (Ctrl+S).
# 2. Confirm git sees it:
git status                            # should list the .ipynb as modified
git diff notebooks/<file>.ipynb | head  # should show your change

# 3. Commit and push:
git add notebooks/<file>.ipynb
git commit -m "study: test note"
git push

# 4. Refresh the file on github.com — your change should appear.
```

If step 2 shows no change, the notebook wasn't saved (the tab title
has a dot when unsaved).

## What syncs from where

| Content | Written by | Where it lands |
|---|---|---|
| NeetCode submissions | NeetCode.io GitHub Sync | `Data Structures & Algorithms/`, `Python For Beginners/` |
| Manual practice | You (locally) | `practice/**` |
| Notebooks and notes | You (locally) | `notebooks/**`, per-problem `NOTES.md` |
| Coursework | You (locally) | `coursework/**` |
| LeetCode auto-sync | Third-party browser extension | A **separate** repo — see [`leetcode_sync.md`](leetcode_sync.md) |

The syncs write to disjoint folders and do not collide, but they can
race on branch tip — that's what the `pull --rebase` habit above
protects against.
