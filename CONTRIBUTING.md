# Contributing

This repository is a personal learning system. External contributions are not
expected, but the same rules apply to the owner when working across multiple
machines.

## Ground rules

1. **Never modify NeetCode-managed files.**
   Anything under `Data Structures & Algorithms/` and `Python For Beginners/`
   is written by NeetCode's GitHub Sync. Do not edit, rename, move, or
   restructure those folders — future syncs may create conflicts or duplicate
   submissions.

2. **All learning infrastructure lives outside sync folders.**
   Notebooks go in `notebooks/`. Manual practice goes in `practice/`.
   Coursework goes in `coursework/`. See `docs/repository_architecture.md`.

3. **No secrets, no credentials, no `.env` files.**
   `.gitignore` protects the common cases; verify before every commit.

4. **No restricted coursework.**
   Do not commit graded exams, answer keys, copyrighted assignment PDFs, or
   solutions to active assessments. See `docs/coursework_privacy.md`.

## Workflow

1. Sync from GitHub before working (`git pull`).
2. Create or update problems using `scripts/create_problem.py` or
   `scripts/create_course_problem.py`.
3. Run tests and validation locally:
   ```bash
   pytest
   ruff check .
   ruff format --check .
   python scripts/validate_repository.py
   ```
4. Update the mastery tracker with `scripts/update_tracker.py`.
5. Commit with a clear, imperative message.
6. Push to GitHub (`git push`).

## Commit style

Use conventional prefixes when adding infrastructure:

- `chore:` — build, config, tooling
- `docs:` — documentation only
- `feat:` — user-visible new capability
- `fix:` — bug fix in a script or notebook
- `test:` — test additions
- `ci:` — GitHub Actions changes
- `study:` — practice work (solutions, notes, tracker updates)

NeetCode-generated commits use their own format (`Add: <problem> - submission-N`).
Do not rewrite those messages.
