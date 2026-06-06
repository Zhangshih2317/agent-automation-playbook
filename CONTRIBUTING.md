# Contributing

This is a personal distilled playbook — but contributions are welcome for:

1. **New projects** that fit the six-theme matrix
2. **Corrections** to existing project deep-dives
3. **Code examples** that demonstrate the techniques
4. **PRO.FILE V8 specific patterns** (the report's primary use case)

## How to add a new project

1. Open an issue with the project's GitHub URL, why it belongs in one of the
   six themes, and your proposed tier (1/2/3)
2. Fork the repo
3. Add the project to:
   - Top of `README.md` project list
   - `docs/NN-project-name.md` (NN = next available number)
   - `skills/<project>/SKILL.md` (Mavis skill format)
   - Update `docs/15-six-themes-matrix.md` (one row in the table)
   - Update `docs/17-decision-tree.md` (if it answers a question)
4. Submit a PR referencing the issue

## SKILL.md format

Each Mavis-loadable skill follows the [Mavis skill spec](https://mavis.dev/docs/skills):

```markdown
---
name: project-name
description: One-line description (triggers Mavis loader)
triggers:
  - "when to invoke"
  - "alternative phrasing"
---

# Project Name

## When to use
[Conditions under which Mavis should load this skill]

## Core technique
[The one core idea you must internalize]

## Minimal code pattern
[5-20 lines of runnable Python]

## PRO.FILE angle
[Specific advice for PRO.FILE V8]

## Pitfalls
[What I got wrong the first time]
```

## Code examples

Each example under `code-examples/<topic>/` should:
- Be runnable with `python main.py` (no fancy deps)
- Print a clear "success" / "result"
- Stay under 200 lines
- Use only `pip install`able deps that exist today
