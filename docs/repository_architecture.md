# Repository Architecture

## Two categories of content

1. **NeetCode-managed.** Written by NeetCode's GitHub Sync. Never edit.
2. **User-maintained.** Everything else.

## Directory purpose

```
Neetcode-Problems/
├── README.md                       User-facing entry point.
├── CONTRIBUTING.md                 Ground rules for repo changes.
├── LICENSE                         MIT for user-authored content.
├── .gitignore                      Excludes venvs, caches, secrets.
├── .gitattributes                  Line endings, notebook diff hints.
├── pyproject.toml                  Project metadata + tool config.
├── requirements-dev.txt            Mirror of the [dev] extras.
├── Makefile                        Convenience commands.
│
├── Data Structures & Algorithms/   NEETCODE-MANAGED. Do not modify.
├── Python For Beginners/           NEETCODE-MANAGED (if present).
│
├── notebooks/                      Topic and per-problem notebooks.
├── practice/                       Manual practice problems.
│   ├── independent/                Solved from scratch.
│   ├── timed/                      Under a time limit.
│   ├── reattempts/                 Later passes at tracked problems.
│   ├── failed_attempts/            Kept as review material.
│   └── pattern_drills/             Short focused drills.
├── coursework/                     Course practice; see coursework_privacy.md
│
├── src/                            Reusable library.
│   ├── algorithms/                 Shared algorithm primitives.
│   ├── visualizations/             Plotting helpers.
│   ├── benchmarking/               Timing helpers.
│   └── utilities/                  Filesystem, slug, tracker.
│
├── tests/                          pytest suite.
│   ├── unit/                       Fast, isolated.
│   └── integration/                Multi-step, still in tmp_path.
│
├── tracking/                       Source of truth for mastery.
│   ├── problem_tracker.csv         The CSV.
│   ├── review_queue.md             Generated.
│   ├── topic_progress.md           Generated.
│   └── schemas/                    JSON Schema for the CSV.
│
├── templates/                      Copy-from-here starters.
├── scripts/                        CLI tools.
├── docs/                           You are here.
└── .github/                        Issue templates, PR template, CI.
```

## Design rules

- **Sync folders are untouchable.** Anything under
  `Data Structures & Algorithms/` and `Python For Beginners/` is
  externally managed. The linter, formatter, and mypy all exclude
  those trees so a rogue submission never breaks CI.
- **Scripts import from `src.utilities`, not each other.** Shared logic
  belongs in `src/`, not `scripts/_helpers.py`.
- **The tracker is the source of truth.** Notebooks and Markdown
  metadata may fall out of sync; the CSV is authoritative.
- **Notebooks stay light.** Heavy computation or large outputs belong
  in a script or a `.py` module.
- **Tests never touch the real tracker.** All fixtures use
  `tmp_path`.
