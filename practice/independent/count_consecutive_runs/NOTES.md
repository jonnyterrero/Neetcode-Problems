# count-consecutive-runs

- **Source:** original (this repository, example)
- **Topic:** arrays-and-hashing
- **Difficulty:** easy
- **Mastery level:** 3

## What this file exists to demonstrate

- Solution + NOTES pair per problem folder.
- A tracker row that references the solution path.
- A `pytest` test that lives alongside the solution.
- A working `python -m` entrypoint (`solution.py` is runnable directly).

## Problem restated

Count the number of maximal consecutive runs of equal values in a sequence.

## Approach

Single pass, track the previous value with a sentinel, increment when the
current value differs. O(n) time, O(1) space.

## Delete me when you have your own work

This example is intentionally trivial. Once you have added real practice
problems, remove `practice/independent/count_consecutive_runs/` (and the
matching row in `tracking/problem_tracker.csv`) if you would prefer a
clean repository.
