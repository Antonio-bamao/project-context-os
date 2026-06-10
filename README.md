# Project Context OS

> Context-first engineering skill that requires a passing `VISION + DESIGN` before implementation.

Project Context OS is an opinionated engineering operating system for agent-assisted software delivery. It makes project memory, design boundaries, structured logs, bug retrospectives, ADRs, and validation gates mandatory before real implementation begins.

The upgraded rule is:

**no implementation without a passing VISION + DESIGN.**

## Why It Exists

Most engineering drift starts before code looks wrong.

Teams and agents skip the user reality, blur scope, invent abstractions, chase popular technology, forget why decisions were made, and resume later from memory instead of a living source of truth.

Project Context OS turns those failure modes into rule violations:

- `vision.md` explains what problem matters, for whom, why, and what is explicitly out of scope.
- `design.md` defines domain boundaries, change axes, interface contracts, technology tradeoffs, NFRs, Walking Skeleton, and de-risk order.
- `validate_context.py` blocks implementation when required design markers or status fields are missing.
- Rotating logs keep long-lived projects readable without losing history.

## What You Get

- A reusable skill at `skills/project-context-os/`
- Scripted initialization of `.context/`
- Design-gated validation before implementation
- Structured append-only work logs with automatic sharding
- Structured bug/issue retrospectives with root causes
- Structured ADR recording with mandatory tradeoffs
- Risk tracking with de-risk order
- A session bootstrap prompt for consistent handoffs
- A generated `INDEX.md` that points new sessions at the active log shards
- A schema and operating model that codify disciplined engineering behavior

## Core Workflow

1. Initialize `.context/` before coding, scaffolding, or refactoring.
2. Fill `vision.md` and `design.md` until validation passes.
3. Start each session from `INDEX.md`, `master-plan.md`, `current-status.md`, the active `work-log` shard, `design.md`, and `operating-model.md`.
4. Produce an implementation plan.
5. Work only on the current task card.
6. Append to the active `work-log` shard after every meaningful step.
7. Record every engineering problem in the active `bug-log` shard with root cause and prevention.
8. Record high-impact choices as ADRs with explicit tradeoffs.
9. Refresh `current-status.md`, including `当前活跃日志分片`.
10. Run validation before declaring context or implementation health.

## Log Rotation

`work-log.md`, `bug-log.md`, and `decisions.md` rotate automatically after `MAX_LOG_LINES = 1500`.

The base file is shard 1:

- `work-log.md`
- `bug-log.md`
- `decisions.md`

Later shards use forward numbering:

- `work-log-2.md`
- `work-log-3.md`

New entries always go to the highest-numbered shard. Rotation happens only between records, so a single work log, bug record, or ADR is never split.

`INDEX.md` is regenerated after initialization and after every append. It lists all shards and the latest active shard for `work-log`, `bug-log`, and `decisions`.

## CLI Examples

```powershell
python skills/project-context-os/scripts/init_context.py --project-root . --project-name "Demo Project"
python skills/project-context-os/scripts/append_work_log.py --project-root . --goal "Walking Skeleton" --actions "Implemented first slice" --result "CLI path works" --verification "python -m unittest" --next-step "Fill current status"
python skills/project-context-os/scripts/record_bug.py --project-root . --title "Validation drift" --symptom "Context passed without design" --trigger "Old schema" --impact "Implementation could start early" --root-cause "No design gate" --resolution "Add required design markers" --prevention "Regression tests" --status "resolved"
python skills/project-context-os/scripts/record_decision.py --project-root . --number "ADR-0001" --title "Use stdlib templates" --status accepted --date "2026-06-11" --context "Templates include JSON braces" --decision "Use string.Template.safe_substitute" --tradeoffs "Gains brace safety; gives up format mini-language" --consequences "Templates use $project_name" --supersedes "无"
python skills/project-context-os/scripts/validate_context.py --project-root .
```

## Repository Layout

```text
project-context-os/
├── README.md
├── LICENSE
├── tests/
└── skills/
    └── project-context-os/
        ├── SKILL.md
        ├── agents/openai.yaml
        ├── scripts/
        ├── references/
        └── assets/
            ├── session-bootstrap.md
            └── templates/
```

## Installation

Copy `skills/project-context-os/` into:

- `$CODEX_HOME/skills`, or
- `~/.codex/skills` when `CODEX_HOME` is unset

Then invoke the skill when a project enters implementation and does not yet have a reliable `.context/` system.

## Design Principles

- **Vision before design**: understand user reality and root cause before shaping the system.
- **Design before code**: domain model, contracts, and tradeoffs are prerequisites.
- **KISS by default**: no abstraction layers, caches, dependencies, or performance work unless the design requires them.
- **YAGNI with a paper trail**: reserve extension points only for changes declared as certain in `design.md`.
- **Structured over narrative**: logs, retrospectives, and ADRs must be queryable and consistent.
- **Decision traceability over folklore**: every high-impact choice records tradeoffs and consequences.
- **Verification before claims**: run validation before saying the context is healthy.

## Chinese / 中文说明

## 这是什么

`Project Context OS` 是一套面向真实工程实施阶段的上下文操作系统 Skill。

新版核心规则是：

**没有通过门禁的 VISION + DESIGN，就不能进入实现。**

它不是普通文档模板，也不是“想起来再写”的项目笔记，而是一套强约束的软件工程方法：

- 开始动工前，必须先建立根目录 `.context/`
- 先写清 `vision.md`：愿景、目标用户、表层诉求与根因、成功定义、非目标、尖锐 FAQ
- 再写清 `design.md`：领域模型、变化轴、接口契约、技术选型、NFR、Walking Skeleton、降险顺序
- `validate_context.py` 不通过，就不能声称上下文健康
- 每完成一个明确步骤，就记录工作日志
- 每遇到工程异常，就记录现象、根因、解决方案和预防措施
- 每做出高影响决策，就追加结构化 ADR，并写明取舍和放弃了什么
- 长日志自动分片，避免一个日志文件无限膨胀

## 适合谁

它适合这些场景：

- 你经常跨会话、多阶段推进项目
- 你不希望项目越做越靠记忆和聊天记录维持
- 你希望 AI/代理在写代码前先想清楚边界
- 你希望 Bug 教训能被沉淀，而不是修完就忘
- 你希望架构决定后面仍然能解释清楚

## 快速理解

你可以把 `.context/` 理解成项目的“工程中枢”：

- `vision.md`：为什么做、为谁做、成功怎么算、什么不做
- `INDEX.md`：所有日志分片和最新活跃分片
- `design.md`：边界、契约、选型、风险和第一条可运行切片
- `master-plan.md`：总计划
- `current-status.md`：当前状态和当前活跃日志分片
- `task-breakdown.md`：任务卡和范围外事项
- `work-log.md` / `work-log-2.md`：工作日志分片
- `bug-log.md` / `bug-log-2.md`：Bug / 工程异常复盘分片
- `decisions.md` / `decisions-2.md`：ADR 分片
- `risk-register.md`：风险台账

只要项目进入真实实施阶段，这套系统就必须先存在，然后持续维护。

## License

MIT
