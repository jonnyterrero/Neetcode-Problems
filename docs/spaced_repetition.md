# Spaced Repetition

The tracker uses a simple, transparent schedule. No neural network, no
opaque scoring — just a table.

## Mastery levels

| Level | Meaning |
|---|---|
| 0 | Unsolved — no valid approach yet. |
| 1 | Assisted — solved with substantial help. |
| 2 | Understood — can explain but not reproduce cold. |
| 3 | Independent — can solve without looking. |
| 4 | Mastered — solves efficiently, explains trade-offs. |
| 5 | Transferable — recognizes and applies the pattern elsewhere. |

## Default intervals

Defined in `src/utilities/tracker.py` as `REVIEW_INTERVAL_DAYS`:

| Mastery | Next review in |
|---|---|
| 0 | 1 day |
| 1 | 1 day |
| 2 | 3 days |
| 3 | 7 days |
| 4 | 21 days |
| 5 | 45 days |

## Adjusting intervals

Edit `REVIEW_INTERVAL_DAYS` in `src/utilities/tracker.py`. Tests will
catch typos. Do not add per-problem overrides — the point is
predictability.

## Reattempts

On every reattempt:

1. Solve the problem **without** looking at the previous solution.
2. If you succeed → keep mastery, or bump it.
3. If you fail → drop mastery by at least 1.
4. Run:

   ```bash
   python scripts/update_tracker.py --problem <slug> --mastery <N> --reviewed --attempt
   ```

`--reviewed` sets today as the last review and reschedules the next
one; `--attempt` increments the attempt count.

## Honesty

The system only works if the tracker reflects reality. Mark a problem
`mastery=3` only if you *just now* solved it independently, not because
you did once, months ago.
