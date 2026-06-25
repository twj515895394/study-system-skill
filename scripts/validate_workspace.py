#!/usr/bin/env python3
"""
校验 study/ 学习工作区的一致性。

用法:
    python "${CLAUDE_SKILL_DIR}/scripts/validate_workspace.py" --root ./study

也可以在 skill 仓库根目录内直接执行:
    python scripts/validate_workspace.py --root ./study

本脚本不修改文件，只做检查并输出 errors/warnings。
"""
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

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

BLOCKING_STATUSES = {"待理解检查", "待补课", "补课中"}

REQUIRED_FILES = [
    "STATE.json",
    "README.md",
    "MISSION.md",
    "MASTER-PLAN.md",
    "TEACHING-PROTOCOL.md",
    "CURRENT.md",
    "PROGRESS.md",
    "COURSE-ROADMAP.md",
    "COURSE-LIST.md",
    "GLOSSARY.md",
    "NOTES.md",
    "QUESTION-PARKING-LOT.md",
    "REVIEW-SCHEDULE.md",
]

REQUIRED_DIRS = [
    "handoffs",
    "lessons",
    "reference",
    "learning-records",
    "exercises",
    "_templates",
]

REQUIRED_WORKSPACE_TEMPLATES = [
    "lesson.md.template",
    "handoff.md.template",
    "learning-record.md.template",
]

HANDOFF_NAME_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}-L\d{2,}-.+\.md$")


class Report:
    def __init__(self) -> None:
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def print(self) -> None:
        if self.errors:
            print("ERRORS:")
            for item in self.errors:
                print(f"  - {item}")
        if self.warnings:
            print("WARNINGS:")
            for item in self.warnings:
                print(f"  - {item}")
        if not self.errors and not self.warnings:
            print("OK: study workspace looks consistent.")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_state(root: Path, report: Report) -> Dict:
    state_path = root / "STATE.json"
    if not state_path.exists():
        report.error("missing STATE.json")
        return {}
    try:
        state = json.loads(read_text(state_path))
    except json.JSONDecodeError as exc:
        report.error(f"STATE.json is not valid JSON: {exc}")
        return {}

    status = state.get("current_status")
    if status not in VALID_STATUSES:
        report.error(f"STATE.json current_status is invalid: {status!r}")

    latest_handoff = state.get("latest_handoff")
    if latest_handoff and not (root / latest_handoff).exists():
        report.error(f"STATE.json latest_handoff does not exist: {latest_handoff}")

    return state


def check_required_paths(root: Path, report: Report) -> None:
    for file_name in REQUIRED_FILES:
        if not (root / file_name).exists():
            report.error(f"missing required file: {file_name}")

    for dir_name in REQUIRED_DIRS:
        path = root / dir_name
        if not path.exists():
            report.error(f"missing required directory: {dir_name}")
        elif not path.is_dir():
            report.error(f"expected directory but found file: {dir_name}")

    for template_name in REQUIRED_WORKSPACE_TEMPLATES:
        if not (root / "_templates" / template_name).exists():
            report.warn(f"missing workspace template: _templates/{template_name}")


def first_content_line_after_heading(text: str, heading: str) -> Optional[str]:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.strip() == heading:
            for candidate in lines[idx + 1 :]:
                stripped = candidate.strip()
                if not stripped:
                    continue
                if stripped.startswith("## "):
                    return None
                return stripped
    return None


def extract_current_status(root: Path, report: Report) -> Optional[str]:
    path = root / "CURRENT.md"
    if not path.exists():
        return None

    line = first_content_line_after_heading(read_text(path), "## 当前状态")
    if line is None:
        report.warn("CURRENT.md has no status under '## 当前状态'")
        return None

    # 初始化模板里的说明行包含多个状态,不能当作真实状态。
    if "使用统一状态" in line or "/" in line:
        report.warn("CURRENT.md still contains the status instruction line; fill one concrete status value")
        return None

    normalized = line.strip("（）() ")
    if normalized in VALID_STATUSES:
        return normalized

    for status in sorted(VALID_STATUSES, key=len, reverse=True):
        if status in line:
            return status

    report.warn(f"CURRENT.md status is not a standard value: {line}")
    return None


def parse_markdown_table(path: Path, expected_min_cols: int, report: Report) -> List[List[str]]:
    if not path.exists():
        return []

    rows: List[List[str]] = []
    for raw_line in read_text(path).splitlines():
        line = raw_line.strip()
        if not line.startswith("|") or not line.endswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if not cells or all(set(cell) <= {"-", ":"} for cell in cells):
            continue
        if cells[0] in {"课次", "编号", "知识点/能力点"}:
            continue
        if len(cells) < expected_min_cols:
            report.warn(f"table row in {path.name} has too few columns: {raw_line}")
            continue
        rows.append(cells)
    return rows


def check_status_tables(root: Path, state: Dict, report: Report) -> None:
    progress_rows = parse_markdown_table(root / "PROGRESS.md", 8, report)
    course_rows = parse_markdown_table(root / "COURSE-LIST.md", 7, report)

    progress_by_lesson = {}
    for row in progress_rows:
        lesson_id = row[0]
        status = row[3]
        learning_record = row[7] if len(row) > 7 else ""
        if status not in VALID_STATUSES:
            report.error(f"PROGRESS.md lesson {lesson_id} has invalid status: {status}")
        if status != "已完成" and learning_record.strip():
            report.error(
                f"PROGRESS.md lesson {lesson_id} has learning-record before completion"
            )
        progress_by_lesson[lesson_id] = status

    course_by_lesson = {}
    for row in course_rows:
        lesson_id = row[0]
        status = row[3]
        if status not in VALID_STATUSES:
            report.error(f"COURSE-LIST.md lesson {lesson_id} has invalid status: {status}")
        course_by_lesson[lesson_id] = status

    for lesson_id, progress_status in progress_by_lesson.items():
        course_status = course_by_lesson.get(lesson_id)
        if course_status and course_status != progress_status:
            report.error(
                f"status mismatch for lesson {lesson_id}: PROGRESS={progress_status}, COURSE-LIST={course_status}"
            )

    current_lesson_id = state.get("current_lesson_id")
    state_status = state.get("current_status")
    if current_lesson_id and str(current_lesson_id) in progress_by_lesson:
        progress_status = progress_by_lesson[str(current_lesson_id)]
        if state_status and state_status != progress_status:
            report.error(
                f"STATE.json status mismatch for current lesson {current_lesson_id}: STATE={state_status}, PROGRESS={progress_status}"
            )


def check_current_state(root: Path, state: Dict, report: Report) -> None:
    current_status = extract_current_status(root, report)
    state_status = state.get("current_status")
    if current_status and state_status and current_status != state_status:
        report.error(f"CURRENT.md status mismatch with STATE.json: CURRENT={current_status}, STATE={state_status}")

    if state_status in BLOCKING_STATUSES:
        report.warn(f"current_status is {state_status}; do not move to the next main lesson before resolving it")


def check_handoffs(root: Path, state: Dict, report: Report) -> None:
    handoffs_dir = root / "handoffs"
    if not handoffs_dir.exists():
        return

    for path in sorted(handoffs_dir.glob("*.md")):
        if not HANDOFF_NAME_PATTERN.match(path.name):
            report.warn(
                f"handoff filename does not follow YYYY-MM-DD-Lxx-slug.md pattern: handoffs/{path.name}"
            )
        status_line = first_content_line_after_heading(read_text(path), "## 本节课状态")
        if status_line:
            matched = any(status in status_line for status in VALID_STATUSES)
            if not matched:
                report.warn(f"handoff {path.name} has non-standard status: {status_line}")

    latest_handoff = state.get("latest_handoff")
    if latest_handoff:
        latest_path = root / latest_handoff
        if latest_path.exists() and latest_path.parent.name != "handoffs":
            report.warn(f"latest_handoff should usually point into handoffs/: {latest_handoff}")


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 study/ 学习工作区一致性")
    parser.add_argument("--root", default="./study", help="工作区根目录,默认 ./study")
    args = parser.parse_args()

    root = Path(args.root)
    report = Report()

    if not root.exists():
        report.error(f"workspace root does not exist: {root}")
        report.print()
        return 1

    check_required_paths(root, report)
    state = load_state(root, report)
    if state:
        check_current_state(root, state, report)
        check_status_tables(root, state, report)
        check_handoffs(root, state, report)

    report.print()
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
