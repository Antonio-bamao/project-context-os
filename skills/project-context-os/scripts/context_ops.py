from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REQUIRED_FILES = (
    "README.md",
    "master-plan.md",
    "current-status.md",
    "task-breakdown.md",
    "work-log.md",
    "bug-log.md",
    "decisions.md",
    "risk-register.md",
)


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    errors: list[str]


def project_context_dir(project_root: Path) -> Path:
    return project_root / ".context"


def template_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "assets" / "templates"


def initialize_context(project_root: Path | str, project_name: str = "Unnamed Project") -> list[Path]:
    root = Path(project_root)
    context_dir = project_context_dir(root)
    context_dir.mkdir(parents=True, exist_ok=True)

    created: list[Path] = []
    for filename in REQUIRED_FILES:
        template_path = template_dir() / filename
        target_path = context_dir / filename
        if target_path.exists():
            continue
        content = template_path.read_text(encoding="utf-8").format(project_name=project_name)
        target_path.write_text(content, encoding="utf-8")
        created.append(target_path)
    return created


def append_work_log(project_root: Path | str, entry: dict[str, str]) -> Path:
    target = project_context_dir(Path(project_root)) / "work-log.md"
    block = (
        f"\n## {entry['time']}｜{entry['goal']}\n"
        f"- 目标：{entry['goal']}\n"
        f"- 动作：{entry['actions']}\n"
        f"- 结果：{entry['result']}\n"
        f"- 验证：{entry['verification']}\n"
        f"- 下一步：{entry['next_step']}\n"
    )
    target.write_text(target.read_text(encoding="utf-8") + block, encoding="utf-8")
    return target


def record_bug(project_root: Path | str, entry: dict[str, str]) -> Path:
    target = project_context_dir(Path(project_root)) / "bug-log.md"
    block = (
        f"\n## {entry['title']}\n"
        f"- 现象：{entry['symptom']}\n"
        f"- 触发条件：{entry['trigger']}\n"
        f"- 影响：{entry['impact']}\n"
        f"- 根因：{entry['root_cause']}\n"
        f"- 解决方案：{entry['resolution']}\n"
        f"- 预防措施：{entry['prevention']}\n"
        f"- 状态：{entry['status']}\n"
    )
    target.write_text(target.read_text(encoding="utf-8") + block, encoding="utf-8")
    return target


def validate_context(project_root: Path | str) -> ValidationResult:
    root = Path(project_root)
    context_dir = project_context_dir(root)
    errors: list[str] = []

    for filename in REQUIRED_FILES:
        target = context_dir / filename
        if not target.exists():
            errors.append(f"missing file: {filename}")

    current_status = context_dir / "current-status.md"
    if current_status.exists():
        content = current_status.read_text(encoding="utf-8")
        if "[待更新]" in content or "TODO" in content:
            errors.append("current-status contains placeholders and must be updated before implementation continues")
        required_lines = ("当前阶段", "已完成", "进行中", "下一步", "阻塞项")
        for field in required_lines:
            if field not in content:
                errors.append(f"current-status missing required field: {field}")

    return ValidationResult(ok=not errors, errors=errors)


def parse_pairs(values: Iterable[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"Invalid key=value pair: {value}")
        key, raw = value.split("=", 1)
        parsed[key] = raw
    return parsed


def build_init_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Initialize a .context engineering operating system.")
    parser.add_argument("--project-root", default=".", help="Project root that should receive .context/")
    parser.add_argument("--project-name", default=None, help="Override project name shown in templates")
    return parser


def build_work_log_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Append a structured work-log entry.")
    parser.add_argument("--project-root", default=".", help="Project root that contains .context/")
    parser.add_argument("--time", required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--actions", required=True)
    parser.add_argument("--result", required=True)
    parser.add_argument("--verification", required=True)
    parser.add_argument("--next-step", required=True)
    return parser


def build_bug_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Append a structured engineering issue retrospective.")
    parser.add_argument("--project-root", default=".", help="Project root that contains .context/")
    parser.add_argument("--title", required=True)
    parser.add_argument("--symptom", required=True)
    parser.add_argument("--trigger", required=True)
    parser.add_argument("--impact", required=True)
    parser.add_argument("--root-cause", required=True)
    parser.add_argument("--resolution", required=True)
    parser.add_argument("--prevention", required=True)
    parser.add_argument("--status", required=True)
    return parser


def build_validate_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate required .context files and fields.")
    parser.add_argument("--project-root", default=".", help="Project root that contains .context/")
    return parser
