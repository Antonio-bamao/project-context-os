import importlib.util
import shutil
import sys
import unittest
import uuid
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "skills" / "project-context-os" / "scripts"


def load_context_ops():
    module_path = SCRIPT_DIR / "context_ops.py"
    spec = importlib.util.spec_from_file_location("context_ops", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load context_ops from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def make_project_dir() -> Path:
    root = REPO_ROOT / "tmp" / f"project-{uuid.uuid4().hex[:8]}"
    root.mkdir(parents=True, exist_ok=True)
    return root


class ContextScriptsTests(unittest.TestCase):
    def write_valid_context(self, project_dir: Path) -> None:
        context_dir = project_dir / ".context"
        (context_dir / "current-status.md").write_text(
            "# 当前状态\n\n"
            "- 当前阶段：Phase 1\n"
            "- 已完成：完成愿景与设计\n"
            "- 进行中：Walking Skeleton\n"
            "- 下一步：执行第一张任务卡\n"
            "- 阻塞项：无\n"
            "- 当前活跃日志分片：work-log.md\n",
            encoding="utf-8",
        )
        (context_dir / "vision.md").write_text(
            "# 产品愿景\n\n"
            "## 一句话愿景\n让上下文成为工程入口。\n\n"
            "## 目标用户与他们的真实处境\n跨会话推进项目的工程师。\n\n"
            "## 表层诉求 vs 根因\n表层诉求：更快开始编码。根因：更快且更可靠地抵达可维护结果。\n\n"
            "## 解法与差异点\n先沉淀愿景、设计和任务边界。\n\n"
            "## 成功定义\n验证命令 100% 通过，且每次会话都能定位最新日志。\n\n"
            "## 非目标 / 明确不做\n不替代项目管理系统。\n\n"
            "## 硬核 FAQ\n问：会不会太重？答：只在进入真实实施时使用。\n",
            encoding="utf-8",
        )
        (context_dir / "design.md").write_text(
            "# 设计说明\n\n"
            "## 0 问题一句话\n缺少设计门禁会导致直接编码。\n\n"
            "## 1 领域模型（核心实体与关系）\nProject 拥有 ContextFile 和 LogShard。\n\n"
            "## 2 可预见的变化轴\n"
            "| 维度 | 当前形态 | 未来可能 | 本次是否预留 | 理由 |\n"
            "| --- | --- | --- | --- | --- |\n"
            "| 日志规模 | 单文件 | 分片 | 是 | 确定会增长 |\n\n"
            "防耦合规则：只为确定会来的变化预留，其余 YAGNI。\n\n"
            "## 3 模块拆分与接口契约\ncontext_ops 输入项目根目录，输出文件路径，不变量是单条记录不拆分。\n\n"
            "## 4 技术选型\n项目真正关心的约束：薄 CLI、无外部依赖、可测试。\n\n"
            "| 选项 | 利 | 弊 | 与约束匹配度 |\n"
            "| --- | --- | --- | --- |\n"
            "| pathlib + stdlib | 稳定 | 功能朴素 | 高 |\n\n"
            "反造火箭自检：当前不是在用火箭解决直升机的问题。\n\n"
            "## 5 非功能需求（NFR）\n校验必须可重复。\n\n"
            "## 6 Walking Skeleton\n初始化、记录、校验穿透所有模块。\n\n"
            "## 7 最高风险与降险顺序（De-risk first）\n先验证分片和门禁。\n",
            encoding="utf-8",
        )
        (context_dir / "master-plan.md").write_text(
            "# Demo Project 总体计划\n\n"
            "## 目标\n交付可验证的上下文操作系统。\n\n"
            "## 非目标 / 明确不做\n不引入外部服务。\n\n"
            "## 阶段与里程碑\n### Phase 1\nWalking Skeleton 可运行。\n\n"
            "## 验收标准\nvalidate_context 通过。\n",
            encoding="utf-8",
        )

    def test_init_context_creates_required_files(self) -> None:
        project_dir = make_project_dir()
        try:
            context_ops = load_context_ops()
            created = context_ops.initialize_context(project_dir, project_name="Demo Project")

            self.assertEqual(
                sorted(path.name for path in created),
                sorted(
                    [
                        "README.md",
                        "INDEX.md",
                        "vision.md",
                        "master-plan.md",
                        "design.md",
                        "current-status.md",
                        "task-breakdown.md",
                        "work-log.md",
                        "bug-log.md",
                        "decisions.md",
                        "risk-register.md",
                    ]
                ),
            )
            self.assertTrue((project_dir / ".context" / "README.md").exists())
        finally:
            shutil.rmtree(project_dir, ignore_errors=True)

    def test_context_index_lists_log_shards_and_updates_after_rotation(self) -> None:
        project_dir = make_project_dir()
        try:
            context_ops = load_context_ops()
            context_ops.initialize_context(project_dir, project_name="Demo Project")
            context_dir = project_dir / ".context"
            index = (context_dir / "INDEX.md").read_text(encoding="utf-8")
            self.assertIn("- work-log：work-log.md", index)
            self.assertIn("- bug-log：bug-log.md", index)
            self.assertIn("- decisions：decisions.md", index)

            (context_dir / "work-log.md").write_text(
                "\n".join(f"line {index}" for index in range(1500)),
                encoding="utf-8",
            )
            context_ops.append_work_log(
                project_dir,
                {
                    "time": "2026-04-07 10:30",
                    "goal": "刷新索引",
                    "actions": "滚动工作日志",
                    "result": "创建第二片",
                    "verification": "检查 INDEX",
                    "next_step": "继续",
                },
            )

            index = (context_dir / "INDEX.md").read_text(encoding="utf-8")
            self.assertIn("- work-log：work-log-2.md", index)
            self.assertIn("- work-log.md", index)
            self.assertIn("- work-log-2.md", index)
        finally:
            shutil.rmtree(project_dir, ignore_errors=True)

    def test_init_context_uses_template_substitution_without_brace_crashes(self) -> None:
        project_dir = make_project_dir()
        try:
            context_ops = load_context_ops()
            context_ops.initialize_context(project_dir, project_name="Brace Demo")

            design = (project_dir / ".context" / "design.md").read_text(encoding="utf-8")
            readme = (project_dir / ".context" / "README.md").read_text(encoding="utf-8")
            self.assertIn("Brace Demo", readme)
            self.assertIn('{"example": "value"}', design)
        finally:
            shutil.rmtree(project_dir, ignore_errors=True)

    def test_append_work_log_adds_structured_entry(self) -> None:
        project_dir = make_project_dir()
        try:
            context_ops = load_context_ops()
            context_ops.initialize_context(project_dir, project_name="Demo Project")
            context_ops.append_work_log(
                project_dir,
                {
                    "time": "2026-04-07 10:30",
                    "goal": "搭建 skill 仓库",
                    "actions": "初始化 tests 与 skill 目录",
                    "result": "完成基础骨架",
                    "verification": "测试红灯出现",
                    "next_step": "补实现",
                },
            )

            text = (project_dir / ".context" / "work-log.md").read_text(encoding="utf-8")
            self.assertIn("搭建 skill 仓库", text)
            self.assertIn("测试红灯出现", text)
            self.assertIn("补实现", text)
        finally:
            shutil.rmtree(project_dir, ignore_errors=True)

    def test_append_work_log_defaults_timestamp_when_time_is_missing(self) -> None:
        project_dir = make_project_dir()
        try:
            context_ops = load_context_ops()
            context_ops.initialize_context(project_dir, project_name="Demo Project")
            context_ops.current_timestamp = lambda: "2026-06-11 12:34"
            parser = context_ops.build_work_log_parser()
            args = parser.parse_args(
                [
                    "--project-root",
                    str(project_dir),
                    "--goal",
                    "自动时间",
                    "--actions",
                    "省略 time 参数",
                    "--result",
                    "脚本补齐",
                    "--verification",
                    "检查日志标题",
                    "--next-step",
                    "继续",
                ]
            )
            context_ops.append_work_log(
                args.project_root,
                {
                    "goal": args.goal,
                    "actions": args.actions,
                    "result": args.result,
                    "verification": args.verification,
                    "next_step": args.next_step,
                },
            )

            text = (project_dir / ".context" / "work-log.md").read_text(encoding="utf-8")
            self.assertIn("## 2026-06-11 12:34｜自动时间", text)
        finally:
            shutil.rmtree(project_dir, ignore_errors=True)

    def test_append_work_log_does_not_rotate_before_threshold(self) -> None:
        project_dir = make_project_dir()
        try:
            context_ops = load_context_ops()
            context_ops.initialize_context(project_dir, project_name="Demo Project")
            work_log = project_dir / ".context" / "work-log.md"
            work_log.write_text("\n".join(f"line {index}" for index in range(1499)), encoding="utf-8")

            target = context_ops.append_work_log(
                project_dir,
                {
                    "time": "2026-04-07 10:30",
                    "goal": "未满阈值",
                    "actions": "追加一条记录",
                    "result": "仍写入首片",
                    "verification": "检查目标路径",
                    "next_step": "继续",
                },
            )

            self.assertEqual(target.name, "work-log.md")
            self.assertFalse((project_dir / ".context" / "work-log-2.md").exists())
            self.assertIn("未满阈值", work_log.read_text(encoding="utf-8"))
        finally:
            shutil.rmtree(project_dir, ignore_errors=True)

    def test_append_work_log_rotates_at_threshold_and_keeps_entry_intact(self) -> None:
        project_dir = make_project_dir()
        try:
            context_ops = load_context_ops()
            context_ops.initialize_context(project_dir, project_name="Demo Project")
            context_dir = project_dir / ".context"
            (context_dir / "work-log.md").write_text(
                "\n".join(f"line {index}" for index in range(1500)),
                encoding="utf-8",
            )

            target = context_ops.append_work_log(
                project_dir,
                {
                    "time": "2026-04-07 10:30",
                    "goal": "跨阈值",
                    "actions": "创建第二片",
                    "result": "完整记录写入新片",
                    "verification": "检查首片不含记录",
                    "next_step": "继续",
                },
            )

            first = (context_dir / "work-log.md").read_text(encoding="utf-8")
            second = (context_dir / "work-log-2.md").read_text(encoding="utf-8")
            self.assertEqual(target.name, "work-log-2.md")
            self.assertNotIn("跨阈值", first)
            self.assertIn("本文件为 work-log.md 第 2 片，续自第 1 片", second)
            self.assertIn("## 2026-04-07 10:30｜跨阈值", second)
            self.assertIn("- 下一步：继续", second)
        finally:
            shutil.rmtree(project_dir, ignore_errors=True)

    def test_active_log_path_uses_largest_existing_shard_after_multiple_rotations(self) -> None:
        project_dir = make_project_dir()
        try:
            context_ops = load_context_ops()
            context_ops.initialize_context(project_dir, project_name="Demo Project")
            context_dir = project_dir / ".context"
            for filename in ("work-log.md", "work-log-2.md"):
                (context_dir / filename).write_text(
                    "\n".join(f"{filename} line {index}" for index in range(1500)),
                    encoding="utf-8",
                )

            target = context_ops.append_work_log(
                project_dir,
                {
                    "time": "2026-04-07 10:30",
                    "goal": "第三片",
                    "actions": "继续滚动",
                    "result": "写入最大序号后一片",
                    "verification": "检查文件名",
                    "next_step": "继续",
                },
            )

            self.assertEqual(target.name, "work-log-3.md")
            self.assertIn("第三片", target.read_text(encoding="utf-8"))
        finally:
            shutil.rmtree(project_dir, ignore_errors=True)

    def test_record_bug_adds_root_cause_and_prevention(self) -> None:
        project_dir = make_project_dir()
        try:
            context_ops = load_context_ops()
            context_ops.initialize_context(project_dir, project_name="Demo Project")
            context_ops.record_bug(
                project_dir,
                {
                    "title": "端口可用性误判",
                    "symptom": "明明端口已占用但仍返回可用",
                    "trigger": "Windows 下端口探测",
                    "impact": "mock runtime 绑定错误",
                    "root_cause": "错误使用 SO_REUSEADDR",
                    "resolution": "移除该选项并重跑测试",
                    "prevention": "加入 Windows 端口占用回归测试",
                    "status": "resolved",
                },
            )

            text = (project_dir / ".context" / "bug-log.md").read_text(encoding="utf-8")
            self.assertIn("错误使用 SO_REUSEADDR", text)
            self.assertIn("加入 Windows 端口占用回归测试", text)
        finally:
            shutil.rmtree(project_dir, ignore_errors=True)

    def test_validate_context_reports_placeholders_until_current_status_is_filled(self) -> None:
        project_dir = make_project_dir()
        try:
            context_ops = load_context_ops()
            context_ops.initialize_context(project_dir, project_name="Demo Project")

            validation = context_ops.validate_context(project_dir)
            self.assertFalse(validation.ok)
            self.assertTrue(any("current-status" in error for error in validation.errors))

            self.write_valid_context(project_dir)
            validation = context_ops.validate_context(project_dir)
            self.assertTrue(validation.ok)
            self.assertEqual(validation.errors, [])
        finally:
            shutil.rmtree(project_dir, ignore_errors=True)

    def test_validate_context_enforces_design_gate(self) -> None:
        project_dir = make_project_dir()
        try:
            context_ops = load_context_ops()
            context_ops.initialize_context(project_dir, project_name="Demo Project")
            self.write_valid_context(project_dir)
            design = project_dir / ".context" / "design.md"
            design.write_text(
                "# 设计说明\n\n"
                "## 1 领域模型（核心实体与关系）\nProject。\n\n"
                "## 2 可预见的变化轴\n[待填]\n\n"
                "## 4 技术选型\nstdlib。\n",
                encoding="utf-8",
            )

            validation = context_ops.validate_context(project_dir)
            self.assertFalse(validation.ok)
            self.assertTrue(any("design.md missing required section: 接口契约" in error for error in validation.errors))
            self.assertTrue(any("design.md contains placeholders" in error for error in validation.errors))

            self.write_valid_context(project_dir)
            validation = context_ops.validate_context(project_dir)
            self.assertTrue(validation.ok)
        finally:
            shutil.rmtree(project_dir, ignore_errors=True)

    def test_append_decision_requires_tradeoff_field(self) -> None:
        project_dir = make_project_dir()
        try:
            context_ops = load_context_ops()
            context_ops.initialize_context(project_dir, project_name="Demo Project")

            with self.assertRaises(ValueError):
                context_ops.append_decision(
                    project_dir,
                    {
                        "number": "ADR-0001",
                        "title": "使用标准库",
                        "status": "accepted",
                        "date": "2026-04-07",
                        "context": "项目需要零依赖。",
                        "decision": "使用 pathlib 和 string.Template。",
                        "consequences": "实现保持朴素。",
                        "supersedes": "无",
                    },
                )
        finally:
            shutil.rmtree(project_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
