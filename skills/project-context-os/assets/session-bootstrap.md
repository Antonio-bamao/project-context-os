# Project Context OS Session Bootstrap

Use this instruction at the start of every implementation session.

1. Read `.context/INDEX.md` to identify the latest active log shards.
2. Read `.context/master-plan.md`.
3. Read `.context/current-status.md`.
4. Read the active work-log shard named in `INDEX.md` / `current-status.md`.
5. Read `.context/design.md`.
6. Read the skill reference `references/operating-model.md`.
7. Produce a short implementation plan before touching code.
8. Work only on the current task card from `.context/task-breakdown.md`.
9. Put new ideas outside the current card into `task-breakdown.md` section `范围外` or `vision.md` section `非目标 / 明确不做`.
10. After meaningful work, append to the active work-log shard with `scripts/append_work_log.py`; omit `--time` unless a precise historical timestamp is needed.
11. Refresh `.context/current-status.md`, including `当前活跃日志分片`.
12. Before closing or claiming health, run `scripts/validate_context.py`.

Do not implement before `vision.md` and `design.md` pass validation.
