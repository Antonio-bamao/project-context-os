# Project Context OS Operating Model

## Purpose

Use `.context/` as the project's execution memory. It is not optional documentation. It is the place where intent, progress, mistakes, and decisions stay synchronized across sessions.

## Mandatory Habits

1. Initialize `.context/` before implementation starts.
2. Read `master-plan.md`, `current-status.md`, and `task-breakdown.md` before doing work.
3. Append to `work-log.md` after every meaningful step.
4. Record every engineering exception in `bug-log.md`, including root cause and prevention.
5. Update `decisions.md` when architecture, delivery, or product constraints change.
6. End every session by refreshing `current-status.md`.

## Anti-Patterns

- Writing code before project memory exists.
- Treating logs as an afterthought.
- Recording only symptoms and not causes.
- Letting `current-status.md` become stale.
- Allowing plans and active work to diverge.
