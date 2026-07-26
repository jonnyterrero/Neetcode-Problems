# Scripts

Every script uses `argparse`, prints its actions, and exits non-zero on
failure so it composes with CI.

| Script | Purpose |
|---|---|
| `create_problem.py` | Scaffold a new independent practice problem. |
| `create_course_problem.py` | Scaffold a new coursework problem. |
| `update_tracker.py` | Update mastery, status, complexity, notes for one problem. |
| `generate_review_queue.py` | Regenerate `tracking/review_queue.md`. |
| `generate_progress_report.py` | Regenerate `tracking/topic_progress.md`. |
| `validate_repository.py` | Check schema, notebook health, and file structure. |
| `clean_notebook_outputs.py` | Strip outputs from tracked notebooks (opt-in). |

## Convention

- All scripts import from `src.utilities` and resolve paths through
  `src.utilities.paths.repo_root()`, so they work from any CWD.
- All scripts have a `--help` flag; consult it before adding new options.
