# Coursework

Practice problems and original notes from programming-heavy university
classes. **Read [`../docs/coursework_privacy.md`](../docs/coursework_privacy.md)
before adding anything here.**

## What belongs here

- Original code you wrote to work through a concept.
- Restated problems (in your own words) that are not under active grading.
- Numerical experiments, plots, and comparisons.
- Class-specific patterns and cheat sheets that do not reproduce copyrighted
  course material.

## What does NOT belong here

- Full copies of graded assignments.
- Active exams or take-home assessments before grades are released.
- Answer keys or restricted solution manuals.
- Copyrighted lecture PDFs, textbook problems, or slides.
- Any material that would violate your school's academic-integrity policy.

Prefer a **private repository** for restricted content. See the privacy
guide for safe patterns and an ignore pattern that keeps a local
`private/` folder out of git.

## Structure

Each course has its own folder. Within a course, group by unit or topic:

```
coursework/<course-slug>/<unit-slug>/<problem-slug>/
    solution.py
    NOTES.md
```

Use `scripts/create_course_problem.py` to scaffold new problems.

## Courses included as starters

The following empty course folders exist so the layout is discoverable.
Rename or remove any that do not match your curriculum.

- `programming_fundamentals/`
- `data_structures_and_algorithms/`
- `discrete_mathematics/`
- `numerical_methods/`
- `biomedical_computing/`
- `machine_learning/`
- `scientific_computing/`
- `other_courses/`
