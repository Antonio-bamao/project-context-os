# 任务拆解

## 里程碑 1：Walking Skeleton

### 任务卡：建立上下文闭环

- 目标：让样例项目具备可验证的 `.context` 最小闭环
- 输入：愿景、设计、状态、任务、日志和风险模板
- 输出：一套可读、可校验的样例 `.context`
- DoD（可自检的完成定义）：`validate_context.py --project-root examples/sample-project` 通过
- 明确不做：不实现真实产品功能
- 规模（S·M·L）：S

## 依赖关系

- `vision.md` 与 `design.md` 通过门禁后，才进入真实功能实现

## 范围外

- 数据库
- 服务端 API
- UI 原型
