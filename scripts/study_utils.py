#!/usr/bin/env python3
"""Shared helpers for study-system workspace scripts."""
import datetime
import json
import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional

VALID_STATUSES = {
    "未开始",
    "进行中",
    "待理解检查",
    "待补课",
    "补课中",
    "已完成",
    "需复习",
    "暂停",
}

PASSING_MASTERY_LEVELS = {"Understanding", "Skill", "Capability"}

LESSON_TYPE_TEMPLATES = {
    "concept": "lesson-types/concept-primer.md.template",
    "concept-primer": "lesson-types/concept-primer.md.template",
    "code": "lesson-types/code-trace.md.template",
    "code-trace": "lesson-types/code-trace.md.template",
    "architecture": "lesson-types/architecture-walkthrough.md.template",
    "architecture-walkthrough": "lesson-types/architecture-walkthrough.md.template",
    "paper": "lesson-types/paper-reading.md.template",
    "paper-reading": "lesson-types/paper-reading.md.template",
    "exercise": "lesson-types/exercise-review.md.template",
    "exercise-review": "lesson-types/exercise-review.md.template",
    "implementation": "lesson-types/implementation-lab.md.template",
    "implementation-lab": "lesson-types/implementation-lab.md.template",
    "phase": "lesson-types/phase-review.md.template",
    "phase-review": "lesson-types/phase-review.md.template",
    "generic": "lesson.md.template",
    "lesson": "lesson.md.template",
}


def today() -> str:
    return datetime.date.today().isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def read_json(path: Path) -> Dict:
    return json.loads(read_text(path))


def write_json(path: Path, data: Dict) -> None:
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def require_workspace(root: Path) -> None:
    if not root.exists():
        raise SystemExit(f"工作区不存在: {root}")
    if not (root / "STATE.json").exists():
        raise SystemExit(f"找不到 STATE.json, 不是有效 study 工作区: {root}")


def validate_status(status: str) -> None:
    if status not in VALID_STATUSES:
        allowed = " / ".join(sorted(VALID_STATUSES))
        raise SystemExit(f"非法状态: {status}。允许值: {allowed}")


def validate_mastery_level(level: str) -> None:
    if level not in PASSING_MASTERY_LEVELS:
        allowed = " / ".join(sorted(PASSING_MASTERY_LEVELS))
        raise SystemExit(f"非法掌握等级: {level}。允许值: {allowed}")


def slugify(value: str, fallback: str = "lesson") -> str:
    value = value.strip().lower()
    value = re.sub(r"[\s_]+", "-", value)
    value = re.sub(r"[^\w\-\u4e00-\u9fff]+", "", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or fallback


def normalize_lesson_id(lesson_id: str) -> str:
    lesson_id = lesson_id.strip()
    if lesson_id.isdigit():
        return f"L{int(lesson_id):02d}"
    return lesson_id


def render_template(text: str, mapping: Dict[str, str]) -> str:
    for key, value in mapping.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def lesson_template_path(root: Path, lesson_type: str) -> Path:
    template_rel = LESSON_TYPE_TEMPLATES.get(lesson_type)
    if template_rel is None:
        allowed = ", ".join(sorted(LESSON_TYPE_TEMPLATES.keys()))
        raise SystemExit(f"未知课型: {lesson_type}。允许值: {allowed}")

    path = root / "_templates" / template_rel
    if path.exists():
        return path

    # 兼容示例工作区使用占位模板,或旧工作区只保留通用模板的情况。
    fallback = root / "_templates" / "lesson.md.template"
    if fallback.exists():
        return fallback

    raise SystemExit(f"找不到课程模板: {path}")


def lesson_output_path(root: Path, lesson_id: str, title: str) -> Path:
    lesson_id = normalize_lesson_id(lesson_id)
    slug = slugify(title, fallback=lesson_id.lower())
    return root / "lessons" / f"{lesson_id}-{slug}.md"


def handoff_output_path(root: Path, lesson_id: str, title: str, date: Optional[str] = None) -> Path:
    lesson_id = normalize_lesson_id(lesson_id)
    date = date or today()
    slug = slugify(title, fallback=lesson_id.lower())
    return root / "handoffs" / f"{date}-{lesson_id}-{slug}.md"


def learning_record_output_path(root: Path, topic: str, slug: Optional[str] = None) -> Path:
    slug = slug or slugify(topic, fallback="learning-record")
    return root / "learning-records" / f"{slug}.md"


def update_state(root: Path, **fields) -> Dict:
    state_path = root / "STATE.json"
    state = read_json(state_path)
    state.update(fields)
    state["last_updated"] = today()
    write_json(state_path, state)
    return state


def replace_section(markdown: str, heading: str, body: str) -> str:
    """Replace a level-2 markdown section body. heading should include '## '."""
    lines = markdown.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == heading:
            start = i
            break
    if start is None:
        body_lines = body.strip("\n").splitlines()
        return markdown.rstrip() + "\n\n" + heading + "\n\n" + "\n".join(body_lines) + "\n"

    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break

    body_lines = [""] + body.strip("\n").splitlines() + [""]
    new_lines = lines[: start + 1] + body_lines + lines[end:]
    return "\n".join(new_lines).rstrip() + "\n"


def update_current_file(
    root: Path,
    lesson_id: Optional[str] = None,
    lesson_title: Optional[str] = None,
    status: Optional[str] = None,
    latest_handoff: Optional[str] = None,
    next_step: Optional[str] = None,
) -> None:
    path = root / "CURRENT.md"
    if not path.exists():
        return

    text = read_text(path)
    if lesson_id or lesson_title:
        lesson_line = " ".join(part for part in [lesson_id, lesson_title] if part)
        text = replace_section(text, "## 当前课程", lesson_line)
    if status:
        text = replace_section(text, "## 当前状态", status)
    if latest_handoff:
        text = replace_section(text, "## 最新 handoff", f"`{latest_handoff}`")
    if next_step:
        text = replace_section(text, "## 下一步", next_step)
    write_text(path, text)


def update_markdown_table_row(
    path: Path,
    lesson_id: str,
    updates: Dict[int, str],
) -> bool:
    """Update a markdown table row by first column. updates maps zero-based column index to value."""
    if not path.exists():
        return False

    lines = read_text(path).splitlines()
    changed = False
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells or cells[0] != lesson_id:
            continue
        for col, value in updates.items():
            if col < len(cells):
                cells[col] = value
        lines[idx] = "| " + " | ".join(cells) + " |"
        changed = True
        break

    if changed:
        write_text(path, "\n".join(lines).rstrip() + "\n")
    return changed


def append_review_schedule_row(
    root: Path,
    topic: str,
    lesson_id: str,
    evidence: str,
    first_review: str = "",
    second_review: str = "",
    status: str = "待复习",
) -> None:
    path = root / "REVIEW-SCHEDULE.md"
    if not path.exists():
        return
    row = f"| {topic} | {today()} | {lesson_id} | {evidence} | {first_review} | {second_review} | {status} |"
    text = read_text(path).rstrip() + "\n" + row + "\n"
    write_text(path, text)


def relative_to_root(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()
