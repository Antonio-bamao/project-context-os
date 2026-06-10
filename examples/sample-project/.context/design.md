# Sample Project 设计说明

## 0 问题一句话

跨会话开发缺少稳定上下文和设计边界，会导致 AI 直接实现、范围漂移和决策失忆。

## 1 领域模型（核心实体与关系）

- Project：被实施的项目根目录。
- ContextFile：`.context/` 下的愿景、设计、计划、状态、任务、风险文件。
- LogShard：可分片的追加日志，包括 work-log、bug-log、decisions。
- TaskCard：当前允许实施的最小任务单元。

Project 拥有多个 ContextFile 和 LogShard；current-status 指向当前活跃 work-log 分片；TaskCard 受 vision 非目标和 design 接口契约约束。

## 2 可预见的变化轴

| 维度 | 当前形态 | 未来可能 | 本次是否预留 | 理由 |
| --- | --- | --- | --- | --- |
| 日志长度 | 单个基础文件 | 多个前向编号分片 | 是 | 长期项目确定会增长 |
| 任务规模 | 单张任务卡 | 多里程碑任务卡 | 否 | 样例只展示最小闭环 |

### 防耦合规则

只为日志长度这种确定会来的变化预留分片；其余一律 YAGNI。预留前先判断复杂度是否来自问题本身。

## 3 模块拆分与接口契约

| 模块 | 输入 | 输出 | 不变量 |
| --- | --- | --- | --- |
| init_context | project root, project name | `.context/` 文件集 | 模板只用 `$project_name` |
| append log | project root, structured entry | active shard path | 单条记录不拆断 |
| validate_context | project root | validation result | 缺设计门禁时失败 |

## 4 技术选型

### 项目真正关心什么约束

样例必须零外部依赖、容易阅读、能在任意 Python 环境运行，并保持 CLI 薄包装。

| 选项 | 利 | 弊 | 与约束匹配度 |
| --- | --- | --- | --- |
| Python stdlib | 无依赖、稳定 | 表达能力朴素 | 高 |
| 外部文档框架 | 功能多 | 增加安装和维护成本 | 低 |

### 反造火箭自检

没有用火箭解决直升机的问题；当前需求是文件模板、追加日志和校验，标准库足够。

## 5 非功能需求（NFR）

- 可移植：不依赖平台特定服务。
- 可验证：验证失败必须返回非零退出。
- 可维护：所有行为集中在 `context_ops.py`。

## 6 Walking Skeleton

初始化 `.context/`，填实 vision/design/status，追加一条 work-log，运行 validate，形成完整闭环。

## 7 最高风险与降险顺序（De-risk first）

| 风险 | 为什么高 | 先验证什么 | 降险动作 |
| --- | --- | --- | --- |
| 直接编码绕过设计 | 会破坏 skill 核心价值 | validate 是否阻止占位和缺章节 | 先写门禁测试 |
| 长日志不可读 | 长期项目必然发生 | 1500 行后是否新建分片 | 分片测试覆盖 |
