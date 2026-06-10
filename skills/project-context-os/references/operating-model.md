# Project Context OS Operating Model

## Purpose

Use `.context/` as the project's execution memory and design gate. It is not optional documentation. It is the place where intent, boundaries, progress, mistakes, and decisions stay synchronized across sessions.

Core rule: no implementation without a passing VISION + DESIGN.

## Mandatory Habits

1. Initialize `.context/` before implementation starts.
2. Fill `vision.md` and `design.md` before implementation starts.
3. Run `scripts/validate_context.py` before claiming the context is healthy or continuing through a design gate.
4. Read `INDEX.md`, `master-plan.md`, `current-status.md`, the active `work-log` shard, `task-breakdown.md`, and `design.md` before doing work.
5. Work only on the current task card.
6. Append to the active `work-log` shard after every meaningful step.
7. Record every engineering exception in the active `bug-log` shard, including root cause and prevention.
8. Append a structured ADR when architecture, delivery, interface contracts, or product constraints change.
9. End every session by refreshing `current-status.md`, including `当前活跃日志分片`.

## Anti-Patterns: Context Discipline

- Writing code before project memory exists.
- Treating logs as an afterthought.
- Recording only symptoms and not causes.
- Letting `current-status.md` become stale.
- Allowing plans and active work to diverge.

## Anti-Patterns: Design And Implementation Discipline

- KISS violation: adding abstraction layers, performance optimization, caching, or third-party dependencies without an explicit requirement.
- Hype-driven selection: choosing technology because it is popular, new, or promises irrelevant QPS instead of following `design.md` section `技术选型`.
- Over-designing for imaginary change: reserving extension points for changes not listed as certain in `design.md` section `可预见的变化轴`.
- Confusing essential complexity with accidental complexity: before adding flexibility, ask whether the complexity belongs to the problem or to the implementation.
- Scope creep: letting a new idea enter implementation before it lands in `vision.md` section `非目标 / 明确不做` or `task-breakdown.md` section `范围外`.
- Silent contract drift: changing any declared interface contract before writing an ADR.
- Unverified success claims: saying "done", "usable", or "healthy" before running `scripts/validate_context.py`.

## Decision Rules

- Decisions have tradeoffs, not absolute correctness.
- A decision record must say what was gained and what was abandoned.
- Interface contracts are binding until an ADR supersedes them.
- Technology choices are subordinate to project constraints, not fashion.

## Change Design Rule

Only design ahead for changes that are certain enough to appear in `design.md` section `可预见的变化轴` with `本次是否预留 = 是`.

Everything else is YAGNI until proven otherwise.
