# Problem-Solving Method

A repeatable sequence to apply to every new problem.

## 1. Restate

Rewrite the problem in your own words. If you cannot, you do not
understand it yet.

## 2. Concrete examples

Write three: small, edge, and adversarial. If the examples in the
problem cover only the happy path, invent your own.

## 3. Enumerate observations

What do the inputs guarantee? What invariants hold? What can you rule
out?

## 4. Brute force first

- State the brute-force approach out loud.
- Compute its complexity.
- Confirm it produces correct output on your examples (mentally or on
  paper).

Only *then* optimize.

## 5. Find the insight

Ask:

- Can I precompute something?
- Can I sort?
- Is there a monotonic property?
- Can two pointers, a hash, or a heap eliminate re-work?
- Can I convert to a known problem (graph, interval, DP)?

## 6. Implement the optimized approach

Keep the brute force in comments (or in a separate cell in the notebook)
so you can compare outputs on the same examples.

## 7. Analyze

- Time complexity — with justification, not a guess.
- Space complexity — including recursion.
- Best / average / worst cases where they differ.

## 8. Enumerate edge cases and test them

- Empty input.
- Single element.
- Duplicates.
- Extreme values.
- Sorted / reverse-sorted input.
- Off-by-one boundaries.

## 9. Explain

If you cannot explain the solution to a peer without notes, mastery is
below 3. Update the tracker honestly.

## 10. Schedule the reattempt

Use `python scripts/update_tracker.py --reviewed --mastery N`. Trust the
schedule.

## Anti-patterns

- Reading the editorial before writing your own attempt.
- Marking a problem "solved" without an independent reattempt.
- Skipping edge cases because "the tests passed."
- Committing without running `pytest` and `ruff`.
