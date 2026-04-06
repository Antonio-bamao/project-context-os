# Project Context OS

> Context-first engineering skill that forces project-level planning, work logs, bug retrospectives, and decision records before implementation.

Project Context OS is an opinionated engineering operating system for agent-assisted software delivery. It makes project memory mandatory by requiring a root-level `.context/` command center before real implementation begins.

Instead of trusting memory, scattered chat history, or half-kept TODOs, this repository gives you a repeatable system for:

- global planning and milestone control
- session-to-session execution continuity
- structured work logging after meaningful steps
- bug and engineering issue retrospectives with root causes
- decision records that preserve architectural intent
- risk tracking that survives implementation pressure

## Why It Exists

Most engineering drift starts long before the code looks wrong.

Plans become vague.
Status becomes implicit.
Bug lessons disappear.
Decisions lose their background.
New sessions resume from memory instead of a living source of truth.

Project Context OS turns that failure mode into a rule violation:

**no implementation without project context.**

## What You Get

- A reusable skill at `skills/project-context-os/`
- Scripted initialization of `.context/`
- Structured append-only work logs
- Structured bug/issue retrospectives
- Context validation before claiming things are “under control”
- A schema and operating model that codify disciplined engineering behavior
- Example `.context/` output for a sample project

## Core Workflow

1. Initialize `.context/` before coding, scaffolding, or refactoring.
2. Read `master-plan.md`, `current-status.md`, and `task-breakdown.md` before each session.
3. Append to `work-log.md` after every meaningful step.
4. Record every engineering problem in `bug-log.md` with root cause and prevention.
5. Update `decisions.md` when high-impact choices are made.
6. Refresh `current-status.md` before ending the session.
7. Run validation before declaring the project context healthy.

## Repository Layout

```text
project-context-os/
├── README.md
├── LICENSE
├── examples/
│   └── sample-project/
│       └── .context/
└── skills/
    └── project-context-os/
        ├── SKILL.md
        ├── agents/openai.yaml
        ├── scripts/
        ├── references/
        └── assets/templates/
```

## Installation

Copy `skills/project-context-os/` into:

- `$CODEX_HOME/skills`, or
- `~/.codex/skills` when `CODEX_HOME` is unset

Then invoke the skill when a project enters implementation and does not yet have a reliable `.context/` system.

## Design Principles

- **Context before code**: project memory is a prerequisite, not an afterthought.
- **Structured over narrative**: logs and retrospectives must be queryable and consistent.
- **Root cause over symptom**: bug records are incomplete without causes and prevention.
- **Session continuity over heroics**: every session should start from explicit state, not recall.
- **Decision traceability over folklore**: architecture should remain explainable after the fact.

## Chinese / 中文说明

## 这是什么

`Project Context OS` 是一套面向真实工程实施阶段的上下文操作系统 Skill。

它不是普通的文档模板，也不是“想起来再写”的项目笔记，而是一套强约束的软件工程方法：

- 开始动工前，必须先建立根目录 `.context/`
- 每次实施前，先看计划、当前状态、任务拆解
- 每完成一个明确步骤，就记录工作日志
- 每遇到一个工程异常，就记录现象、根因、解决方案和预防措施
- 每做出高影响决策，就留下决策记录
- 每次会话结束前，必须更新当前状态

## 适合谁

它适合这些场景：

- 你经常跨会话、多阶段推进项目
- 你不希望项目越做越靠记忆和聊天记录维持
- 你希望 Bug 教训能被沉淀，而不是修完就忘
- 你希望 AI/代理参与开发时也遵守工程纪律，而不是“做一步想一步”

## 它解决什么问题

它解决的是软件工程里最常见但最容易被忽略的问题：

- 项目有代码，没有可持续的上下文
- 每次开新会话都要重新解释背景
- 计划写过，但没有持续跟进
- Bug 修掉了，但不知道为什么会发生
- 架构决定做过了，后面的人却不知道原因

`Project Context OS` 把这些问题前置为工程规则，而不是事后补救。

## 快速理解

你可以把 `.context/` 理解成项目的“工程中枢”：

- `master-plan.md`：总计划
- `current-status.md`：当前状态
- `task-breakdown.md`：任务拆解
- `work-log.md`：工作日志
- `bug-log.md`：Bug / 工程异常复盘
- `decisions.md`：决策记录
- `risk-register.md`：风险台账

只要项目进入真实实施阶段，这套系统就必须先存在，然后持续维护。

## License

MIT
