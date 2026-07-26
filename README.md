# NeetCode-Problems — Programming Practice & Computational Learning System

A personal, long-term learning system built on top of a
[NeetCode.io](https://neetcode.io) GitHub-synchronized submissions repository.

**Profiles:**
[LeetCode: jterrero16](https://leetcode.com/u/jterrero16/) ·
[NeetCode](https://neetcode.io)

This repository stores:

- **NeetCode-synchronized solutions** — written on neetcode.io and pushed here automatically.
- **Manual LeetCode / independent practice** — solutions written locally.
- **Jupyter notebooks** — topic overviews, algorithm visualizations, worked examples, mistakes, and pattern notes.
- **Coursework practice** — original problems and notes from programming-heavy university classes.
- **Tests** — small, focused tests for shared utilities and template problems.
- **A mastery tracker** — CSV-based record of every problem, its mastery level, and its next review date.
- **Automation scripts** — for creating problems, updating mastery, generating review queues, and validating the repo.

---

## Managed vs. manual content

This repository has two categories of content that must not be confused:

### NeetCode-managed content (do not edit)

Written by NeetCode's GitHub Sync. Do not rename, move, or edit these files.

```
Data Structures & Algorithms/
    <problem-slug>/
        submission-0.<ext>
        submission-1.<ext>
        ...

Python For Beginners/
    <problem-slug>/
        submission-0.<ext>
```

### User-maintained learning content

Everything below is added and maintained by you.

```
notebooks/     Topic notebooks and worked examples
practice/      Manual / independent practice problems
coursework/    Programming-heavy university course practice
src/           Shared algorithms, visualizations, benchmarks, utilities
tests/         Tests for utilities, templates, scripts
tracking/      Mastery tracker + review queue + topic progress
templates/     Solution, notebook, and test templates
scripts/       CLI tools for creating problems and generating reports
docs/          Full documentation
.github/       Issue templates, PR template, CI workflows
```

See [`docs/repository_architecture.md`](docs/repository_architecture.md) for
the full picture.

---

## Getting started

### 1. Clone

```bash
git clone https://github.com/jonnyterrero/Neetcode-Problems.git
cd Neetcode-Problems
```

### 2. Create a virtual environment

**macOS / Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (cmd):**

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

### 3. Install dev dependencies

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

### 4. Launch Jupyter (optional)

```bash
jupyter lab
```

### 5. Run the test suite

```bash
pytest
```

See [`docs/setup.md`](docs/setup.md) for the full setup guide, including
`make` targets and troubleshooting.

---

## VS Code workflow

1. Install the **Python** and **Jupyter** extensions.
2. Open the repository folder.
3. `Ctrl+Shift+P` → **Python: Select Interpreter** → choose the `.venv`.
4. Open any `.ipynb` file from `notebooks/`.
5. Choose the matching kernel when prompted.
6. Run cells with `Shift+Enter`.
7. Commit and push through the built-in Source Control panel.

---

## Daily workflow

```
Attempt → Implement → Test → Explain → Track → Review → Commit
```

Concretely:

1. Attempt the problem without assistance.
2. Record your first-pass reasoning in the topic notebook.
3. Write a clean solution in `practice/independent/<slug>/solution.py`.
4. Add local tests and run `pytest`.
5. If stuck, study the pattern; capture what unlocked the solution.
6. Update mastery with `python scripts/update_tracker.py`.
7. Let the review scheduler tell you when to reattempt.
8. Commit with a short message and push.

See [`docs/workflow.md`](docs/workflow.md) for details.

---

## Multi-device workflow

Before starting on a machine:

```bash
git pull
```

After a session:

```bash
git add .
git commit -m "study: <what you did>"
git push
```

Because NeetCode's GitHub Sync can also push commits from the web editor,
always `git pull` before starting to avoid divergent history.

---

## Cloud access

GitHub is the permanent source of truth. Notebooks can be executed:

- **Locally** in VS Code or JupyterLab (recommended).
- **In GitHub Codespaces** if you want a full cloud dev environment.
- **In Google Colab** for one-off notebook execution (data does not persist).

See [`docs/cloud_access.md`](docs/cloud_access.md) for trade-offs.

## LeetCode auto-sync

LeetCode has no first-party GitHub sync. If you want submissions on
[leetcode.com/u/jterrero16](https://leetcode.com/u/jterrero16/) to push
to a repo automatically, install a community browser extension
(LeetHub v2 or LeetSync) and point it at a **separate** repo so it
doesn't collide with NeetCode Sync here. Full setup in
[`docs/leetcode_sync.md`](docs/leetcode_sync.md).

---

## Coursework privacy

University coursework is often subject to academic-integrity policies and
copyright restrictions. **Do not commit graded assessments, answer keys, or
copyrighted assignment PDFs to a public repository.**

See [`docs/coursework_privacy.md`](docs/coursework_privacy.md) for the full
policy and safe patterns.

---

## Automation cheat sheet

```bash
# Create a new independent practice problem
python scripts/create_problem.py \
  --name "Container With Most Water" \
  --source leetcode --topic two-pointers --difficulty medium

# Create a new coursework problem
python scripts/create_course_problem.py \
  --course numerical-methods --unit root-finding \
  --name "Newton Method Convergence"

# Update the mastery tracker
python scripts/update_tracker.py \
  --problem "container-with-most-water" --mastery 3 --status solved

# Generate a Markdown review queue
python scripts/generate_review_queue.py

# Generate a Markdown progress report
python scripts/generate_progress_report.py

# Validate the repository
python scripts/validate_repository.py
```

---

## Supported languages

Python is the primary language. The system is designed to accept others:

| Language | Extension |
|---|---|
| Python | `.py` |
| JavaScript | `.js` |
| TypeScript | `.ts` |
| Java | `.java` |
| C++ | `.cpp` |
| C# | `.cs` |
| Go | `.go` |
| Rust | `.rs` |
| Kotlin | `.kt` |
| Swift | `.swift` |
| SQL | `.sql` |
| MATLAB | `.m` |

---

## About NeetCode Sync

[NeetCode.io](https://neetcode.io) is a coding-interview preparation
platform. Every time a solution is submitted on neetcode.io, GitHub Sync
pushes it here automatically, under the `Data Structures & Algorithms/`
or `Python For Beginners/` folders. Sync preferences are managed at
[neetcode.io/profile/github](https://neetcode.io/profile/github).

*This README extends the original NeetCode-generated one to describe the
learning system built around the synchronized submissions.*
