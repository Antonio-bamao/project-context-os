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
                        "master-plan.md",
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

            current_status = project_dir / ".context" / "current-status.md"
            current_status.write_text(
                "# 当前状态\n\n"
                "- 当前阶段：Phase 1\n"
                "- 已完成：完成 skill 仓库骨架设计\n"
                "- 进行中：补脚本实现\n"
                "- 下一步：完成 README 与示例\n"
                "- 阻塞项：无\n",
                encoding="utf-8",
            )

            validation = context_ops.validate_context(project_dir)
            self.assertTrue(validation.ok)
            self.assertEqual(validation.errors, [])
        finally:
            shutil.rmtree(project_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
