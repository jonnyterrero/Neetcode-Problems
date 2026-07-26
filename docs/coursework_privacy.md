# Coursework Privacy

This repository is public. Academic-integrity rules and copyright do
not stop applying just because the file is in `coursework/`.

## Do not commit

- Full copies of graded assignments, take-home exams, or midterms.
- Answer keys or restricted solution manuals.
- Copyrighted lecture PDFs, textbook problems, or slide decks.
- Anything that identifies other students by name.
- Anything you are contractually or academically prohibited from
  redistributing.

## Prefer a private repository

For content that must be kept restricted, use a **separate private
repository**. Do not mix restricted content into this public repo and
hope `.gitignore` covers it.

## Safe patterns

- Restate the problem in your own words before committing.
- Store only your original code and your original notes.
- Reference textbook problems by chapter and problem number instead of
  pasting the full text.
- Store numeric results and plots, not the raw restricted dataset.

## Local-only content

If you must keep restricted content on disk without pushing it, use a
`private/` subfolder inside any coursework directory. `.gitignore`
already excludes:

```
coursework/**/private/
coursework/**/_private/
coursework/**/*.private.*
coursework/**/*_solutions_key.*
coursework/**/*answer_key*
coursework/**/exams/
```

Verify before every commit:

```bash
git status
```

If anything sensitive appears staged, unstage it (`git restore --staged
<file>`) and move it under a `private/` folder.

## What the validator does

`scripts/validate_repository.py` scans `coursework/` for filenames that
look restricted (`answer_key`, `midterm-`, `final-exam`, etc.) and
warns. Warnings are not failures by default — pass `--strict` to make
them fatal.
