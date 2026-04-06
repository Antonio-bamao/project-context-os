---
name: project-context-os
description: Use when a project is entering real implementation work and needs a mandatory .context operating system before coding, scaffolding, refactoring, or feature delivery. Trigger when starting a new project, opening a repo with missing project context files, or when ongoing work lacks a master plan, current status, work log, bug retrospectives, or decision records.
---

# Project Context OS

## Overview

Force context-first engineering. Before any real implementation work, create or repair a project-root `.context/` system, then keep plans, current status, work logs, bug retrospectives, decision records, and risk tracking continuously updated.

**Core principle:** no implementation without project memory.

## Workflow

1. Before writing code, check whether `.context/README.md`, `.context/master-plan.md`, `.context/current-status.md`, and `.context/task-breakdown.md` exist.
2. If `.context/` is missing or incomplete, run `scripts/init_context.py` from this skill against the project root before continuing.
3. Read `.context/master-plan.md`, `.context/current-status.md`, and `.context/task-breakdown.md` before deciding the next implementation step.
4. After each meaningful step, append to `.context/work-log.md` using `scripts/append_work_log.py`.
5. When any engineering problem appears, record it in `.context/bug-log.md` using `scripts/record_bug.py`.
6. When a high-impact technical or product choice is made, update `.context/decisions.md`.
7. At the end of every work session, update `.context/current-status.md` with current state, next step, and blockers.
8. Run `scripts/validate_context.py` before claiming the project context is healthy.

## Required Files

- `.context/README.md`: explain how the context system works in the project.
- `.context/master-plan.md`: global plan, phases, milestones, acceptance criteria.
- `.context/current-status.md`: latest state, active work, next step, blockers.
- `.context/task-breakdown.md`: actionable decomposition and priorities.
- `.context/work-log.md`: append-only structured execution log.
- `.context/bug-log.md`: engineering errors, root causes, fixes, preventions.
- `.context/decisions.md`: architecture and product decisions.
- `.context/risk-register.md`: project risk tracking and mitigations.

## Scripts

- `scripts/init_context.py`: initialize the `.context/` command center from templates.
- `scripts/append_work_log.py`: append a structured work-log entry after each meaningful step.
- `scripts/record_bug.py`: append a structured bug or engineering issue retrospective.
- `scripts/validate_context.py`: verify required files exist and critical placeholders are removed.

## References

- Read `references/operating-model.md` for the governing engineering model and required habits.
- Read `references/context-schema.md` for required sections, field meanings, and update rules.

## Common Mistakes

- Starting implementation after creating `.context/`, but before filling `current-status`: not allowed. Update the status file immediately.
- Writing free-form diary notes instead of structured logs: always use the required fields.
- Recording only the symptom of a bug: always include root cause and prevention.
- Letting `master-plan` drift away from `current-status`: keep them aligned whenever scope changes.
- Treating `.context/` as optional documentation: it is the project operating system, not a nice-to-have.

## Quick Reference

- New project starting: run `scripts/init_context.py`.
- Meaningful step finished: run `scripts/append_work_log.py`.
- Error or engineering pitfall hit: run `scripts/record_bug.py`.
- Before declaring the project context healthy: run `scripts/validate_context.py`.

## Resources

- Templates live in `assets/templates/`.
- Policy and schema details live in `references/`.
- All project mutations should happen through the scripts or through direct edits that keep the same structure.
