# Notebooks

Structured Jupyter notebooks for each major topic on the NeetCode roadmap.

## Purpose

- Explain patterns.
- Visualize algorithms.
- Compare approaches.
- Record mistakes.
- Benchmark.
- Connect algorithms to coursework and engineering applications.

Notebooks are for *learning*. Clean `.py` files under `practice/` remain
the source of truth for tested implementations.

## Files

Numbered in the order the NeetCode roadmap introduces them:

| # | Notebook | Topic |
|---|---|---|
| 01 | `01_arrays_and_hashing.ipynb` | Arrays and hashing |
| 02 | `02_two_pointers.ipynb` | Two pointers |
| 03 | `03_sliding_window.ipynb` | Sliding window |
| 04 | `04_stack.ipynb` | Stacks |
| 05 | `05_binary_search.ipynb` | Binary search |
| 06 | `06_linked_lists.ipynb` | Linked lists |
| 07 | `07_trees.ipynb` | Trees |
| 08 | `08_tries.ipynb` | Tries |
| 09 | `09_heap_priority_queue.ipynb` | Heaps and priority queues |
| 10 | `10_backtracking.ipynb` | Backtracking |
| 11 | `11_graphs.ipynb` | Graphs |
| 12 | `12_advanced_graphs.ipynb` | Advanced graph algorithms |
| 13 | `13_dynamic_programming_1d.ipynb` | 1D dynamic programming |
| 14 | `14_dynamic_programming_2d.ipynb` | 2D dynamic programming |
| 15 | `15_greedy.ipynb` | Greedy |
| 16 | `16_intervals.ipynb` | Intervals |
| 17 | `17_math_and_geometry.ipynb` | Math and geometry |
| 18 | `18_bit_manipulation.ipynb` | Bit manipulation |

## Conventions

- **Do not** paste full LeetCode / NeetCode problem statements into these
  notebooks. Restate briefly in your own words or link out.
- Keep outputs small. Use `scripts/clean_notebook_outputs.py` before
  committing if a run produced large plots or data dumps.
- Use `src/algorithms/`, `src/visualizations/`, and `src/benchmarking/`
  for anything you would otherwise copy-paste between notebooks.
