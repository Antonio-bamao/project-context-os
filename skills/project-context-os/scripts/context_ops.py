from __future__ import annotations

import argparse
import re
from datetime import datetime
from string import Template
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REQUIRED_FILES = (
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
)

MAX_LOG_LINES = 1500
ROTATING_LOGS = ("work-log.md", "bug-log.md", "decisions.md")
PLACEHOLDERS = ("[待更新]", "TODO", "[待填]")


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
        content = Template(template_path.read_text(encoding="utf-8")).safe_substitute(project_name=project_name)
        target_path.write_text(content, encoding="utf-8")
        created.append(target_path)
    update_context_index(context_dir)
    return created


def current_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def line_count(path: Path) -> int:
    if not path.exists():
        return 0
    content = path.read_text(encoding="utf-8")
    if content == "":
        return 0
    return content.count("\n") + 1


def log_shard_number(base_name: str, path: Path) -> int | None:
    base_path = Path(base_name)
    if path.name == base_name:
        return 1
    pattern = rf"^{re.escape(base_path.stem)}-(\d+){re.escape(base_path.suffix)}$"
    match = re.match(pattern, path.name)
    if match is None:
        return None
    number = int(match.group(1))
    if number < 2:
        return None
    return number


def log_shards(context_dir: Path, base_name: str) -> list[tuple[int, Path]]:
    base_path = Path(base_name)
    matches: list[tuple[int, Path]] = []
    for path in context_dir.glob(f"{base_path.stem}*{base_path.suffix}"):
        number = log_shard_number(base_name, path)
        if number is not None:
            matches.append((number, path))
    return sorted(matches, key=lambda item: item[0])


def active_log_path(context_dir: Path, base_name: str, for_write: bool = True) -> Path:
    shards = log_shards(context_dir, base_name)
    if not shards:
        return context_dir / base_name

    last_number, last_path = shards[-1]
    if for_write and line_count(last_path) >= MAX_LOG_LINES:
        next_number = last_number + 1
        next_path = context_dir / f"{Path(base_name).stem}-{next_number}{Path(base_name).suffix}"
        if not next_path.exists():
            next_path.write_text(
                f"# {base_name} 第 {next_number} 片\n\n"
                f"> 本文件为 {base_name} 第 {next_number} 片，续自第 {next_number - 1} 片。\n",
                encoding="utf-8",
            )
        return next_path
    return last_path


def append_block(target: Path, block: str) -> None:
    existing = target.read_text(encoding="utf-8") if target.exists() else ""
    target.write_text(existing + block, encoding="utf-8")


def update_context_index(context_dir: Path) -> Path:
    index_path = context_dir / "INDEX.md"
    active_lines: list[str] = []
    shard_sections: list[str] = []
    for base_name in ROTATING_LOGS:
        shards = log_shards(context_dir, base_name)
        shard_names = [path.name for _, path in shards] or [base_name]
        active_name = shard_names[-1]
        label = Path(base_name).stem
        active_lines.append(f"- {label}：{active_name}")
        shard_sections.append(
            f"### {base_name}\n\n" + "\n".join(f"- {name}" for name in shard_names)
        )

    content = (
        "# .context INDEX\n\n"
        "> 机器生成的上下文入口清单。日志追加脚本会自动刷新本文件。\n\n"
        "## 最新活跃分片\n\n"
        + "\n".join(active_lines)
        + "\n\n## 所有日志分片\n\n"
        + "\n\n".join(shard_sections)
        + "\n\n## 关键入口\n\n"
        "- vision.md\n"
        "- design.md\n"
        "- master-plan.md\n"
        "- current-status.md\n"
        "- task-breakdown.md\n"
        "- risk-register.md\n"
    )
    index_path.write_text(content, encoding="utf-8")
    return index_path


def append_work_log(project_root: Path | str, entry: dict[str, str]) -> Path:
    context_dir = project_context_dir(Path(project_root))
    target = active_log_path(context_dir, "work-log.md")
    entry_time = entry.get("time") or current_timestamp()
    block = (
        f"\n## {entry_time}｜{entry['goal']}\n"
        f"- 目标：{entry['goal']}\n"
        f"- 动作：{entry['actions']}\n"
        f"- 结果：{entry['result']}\n"
        f"- 验证：{entry['verification']}\n"
        f"- 下一步：{entry['next_step']}\n"
    )
    append_block(target, block)
    update_context_index(context_dir)
    return target


def record_bug(project_root: Path | str, entry: dict[str, str]) -> Path:
    context_dir = project_context_dir(Path(project_root))
    target = active_log_path(context_dir, "bug-log.md")
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
    append_block(target, block)
    update_context_index(context_dir)
    return target


def append_decision(project_root: Path | str, entry: dict[str, str]) -> Path:
    required = (
        "number",
        "title",
        "status",
        "date",
        "context",
        "decision",
        "tradeoffs",
        "consequences",
        "supersedes",
    )
    missing = [field for field in required if not entry.get(field)]
    if missing:
        raise ValueError(f"missing decision field(s): {', '.join(missing)}")
    if entry["status"] not in {"proposed", "accepted", "superseded"}:
        raise ValueError("decision status must be one of: proposed, accepted, superseded")

    context_dir = project_context_dir(Path(project_root))
    target = active_log_path(context_dir, "decisions.md")
    block = (
        f"\n## {entry['number']}：{entry['title']}\n"
        f"- 状态：{entry['status']}\n"
        f"- 日期：{entry['date']}\n"
        f"- 背景（Context）：{entry['context']}\n"
        f"- 决策（Decision）：{entry['decision']}\n"
        f"- 取舍（利弊，放弃了什么）：{entry['tradeoffs']}\n"
        f"- 后果（Consequences）：{entry['consequences']}\n"
        f"- 取代关系（Supersedes）：{entry['supersedes']}\n"
    )
    append_block(target, block)
    update_context_index(context_dir)
    return target


def contains_placeholder(content: str) -> bool:
    return any(placeholder in content for placeholder in PLACEHOLDERS)


def validate_context(project_root: Path | str) -> ValidationResult:
    root = Path(project_root)
    context_dir = project_context_dir(root)
    errors: list[str] = []

    for filename in REQUIRED_FILES:
        if filename in ROTATING_LOGS:
            if not log_shards(context_dir, filename):
                errors.append(f"missing file: {filename}")
            continue
        if not (context_dir / filename).exists():
            errors.append(f"missing file: {filename}")

    current_status = context_dir / "current-status.md"
    if current_status.exists():
        content = current_status.read_text(encoding="utf-8")
        if contains_placeholder(content):
            errors.append("current-status contains placeholders and must be updated before implementation continues")
        required_lines = ("当前阶段", "已完成", "进行中", "下一步", "阻塞项", "当前活跃日志分片")
        for field in required_lines:
            if field not in content:
                errors.append(f"current-status missing required field: {field}")
        active_work_log = active_log_path(context_dir, "work-log.md", for_write=False).name
        if "当前活跃日志分片" in content and active_work_log not in content:
            errors.append(f"current-status must point to active work-log shard: {active_work_log}")

    design = context_dir / "design.md"
    if design.exists():
        content = design.read_text(encoding="utf-8")
        if contains_placeholder(content):
            errors.append("design.md contains placeholders and must be completed before implementation continues")
        for marker in ("领域模型", "可预见的变化轴", "接口契约", "选型"):
            if marker not in content:
                errors.append(f"design.md missing required section: {marker}")

    vision = context_dir / "vision.md"
    if vision.exists():
        content = vision.read_text(encoding="utf-8")
        for marker in ("成功定义", "非目标"):
            if marker not in content:
                errors.append(f"vision.md missing required section: {marker}")

    master_plan = context_dir / "master-plan.md"
    if master_plan.exists() and "非目标" not in master_plan.read_text(encoding="utf-8"):
        errors.append("master-plan.md missing required section: 非目标")

    index = context_dir / "INDEX.md"
    if index.exists():
        content = index.read_text(encoding="utf-8")
        if contains_placeholder(content):
            errors.append("INDEX.md contains placeholders and must be regenerated")
        for filename in ROTATING_LOGS:
            shards = log_shards(context_dir, filename)
            if not shards:
                continue
            active = shards[-1][1].name
            if active not in content:
                errors.append(f"INDEX.md missing active shard: {active}")
            for _, shard in shards:
                if shard.name not in content:
                    errors.append(f"INDEX.md missing log shard: {shard.name}")

    for filename in ROTATING_LOGS:
        shards = log_shards(context_dir, filename)
        if not shards:
            continue
        active = shards[-1][1]
        if contains_placeholder(active.read_text(encoding="utf-8")):
            errors.append(f"{active.name} contains placeholders and must be updated")

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
    parser.add_argument("--time", default=None, help="Entry timestamp; defaults to current local time")
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


def build_decision_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Append a structured architecture decision record.")
    parser.add_argument("--project-root", default=".", help="Project root that contains .context/")
    parser.add_argument("--number", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--status", choices=("proposed", "accepted", "superseded"), required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--context", required=True)
    parser.add_argument("--decision", required=True)
    parser.add_argument("--tradeoffs", required=True)
    parser.add_argument("--consequences", required=True)
    parser.add_argument("--supersedes", required=True)
    return parser


def build_validate_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate required .context files and fields.")
    parser.add_argument("--project-root", default=".", help="Project root that contains .context/")
    return parser
