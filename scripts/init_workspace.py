#!/usr/bin/env python3
"""
初始化一个 study/ 学习工作区骨架。

用法:
    python "${CLAUDE_SKILL_DIR}/scripts/init_workspace.py" --root ./study --topic "RAG 系统原理" --domain code

也可以在 skill 仓库根目录内直接执行:
    python scripts/init_workspace.py --root ./study --topic "RAG 系统原理" --domain code

domain 接受任意字符串。code/course/industry/exam/child 是5个常见预设(决定资料
地图文件名),命中即用对应命名;不在预设里的领域(比如"研究资料阅读""技能训练""产品
体系学习")不会报错——会落到通用命名 RESOURCE-READING-MAP.md,也可以用
--reading-map-name / --reading-map-title 完全自定义文件名和标题。
不要因为某个学习场景"不属于这5类"就为难,这几个预设只是省事的别名,不是穷举。
"""
import argparse
import datetime
import json
import os
from pathlib import Path

DOMAIN_READING_MAP = {
    "code": ("SOURCE-READING-MAP.md", "源码阅读地图"),
    "course": ("TEXTBOOK-READING-MAP.md", "教材阅读地图"),
    "industry": ("RESOURCE-READING-MAP.md", "资料阅读地图"),
    "exam": ("EXAM-ROADMAP.md", "题型与章节地图"),
    "child": ("SCHOOL-SYNC-PLAN.md", "学校进度同步地图"),
}

DEFAULT_READING_MAP = ("RESOURCE-READING-MAP.md", "资料阅读地图")

SUBDIRS = [
    "handoffs",
    "lessons",
    "reference",
    "learning-records",
    "exercises",
    "_templates",
    "_templates/lesson-types",
]

# (输出文件名, 模板文件名)
FILE_MAP = [
    ("README.md", "README.md.template"),
    ("MASTER-PLAN.md", "MASTER-PLAN.md.template"),
    ("MISSION.md", "MISSION.md.template"),
    ("CURRENT.md", "CURRENT.md.template"),
    ("PROGRESS.md", "PROGRESS.md.template"),
    ("COURSE-ROADMAP.md", "COURSE-ROADMAP.md.template"),
    ("COURSE-LIST.md", "COURSE-LIST.md.template"),
    ("TEACHING-PROTOCOL.md", "TEACHING-PROTOCOL.md.template"),
    ("GLOSSARY.md", "GLOSSARY.md.template"),
    ("NOTES.md", "NOTES.md.template"),
    ("QUESTION-PARKING-LOT.md", "QUESTION-PARKING-LOT.md.template"),
    ("REVIEW-SCHEDULE.md", "REVIEW-SCHEDULE.md.template"),
]

# 复制到 study/_templates/ 的模板。这里保留模板占位符,供后续课程/交接/学习记录创建时使用。
WORKSPACE_TEMPLATE_FILES = [
    "lesson.md.template",
    "handoff.md.template",
    "learning-record.md.template",
    "review-quiz.md.template",
    "lesson-types/concept-primer.md.template",
    "lesson-types/code-trace.md.template",
    "lesson-types/architecture-walkthrough.md.template",
    "lesson-types/paper-reading.md.template",
    "lesson-types/exercise-review.md.template",
    "lesson-types/implementation-lab.md.template",
    "lesson-types/phase-review.md.template",
]


def render(text: str, mapping: dict) -> str:
    for key, value in mapping.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def get_skill_dir() -> Path:
    """返回 skill 根目录。

    在 Claude Code Skill 环境中优先使用 CLAUDE_SKILL_DIR；在本仓库内直接执行时，
    回退到脚本所在目录的上级目录。这样文档中的安装式调用和开发式调用都能工作。
    """
    env_skill_dir = os.environ.get("CLAUDE_SKILL_DIR")
    if env_skill_dir:
        return Path(env_skill_dir).expanduser().resolve()
    return Path(__file__).resolve().parent.parent


def write_initial_state(root: Path, args, reading_map_filename: str, today: str, created: list, skipped: list) -> None:
    state_path = root / "STATE.json"
    if state_path.exists():
        skipped.append(str(state_path))
        return

    state = {
        "schema_version": 1,
        "topic": args.topic,
        "domain": args.domain,
        "reading_map": reading_map_filename,
        "diagnosis_mode": args.diagnosis_mode,
        "current_lesson_id": None,
        "current_lesson_title": None,
        "current_phase": None,
        "current_status": "未开始",
        "latest_handoff": None,
        "blocked_by": [],
        "makeup_count_in_current_phase": 0,
        "last_updated": today,
    }
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    created.append(str(state_path))


def copy_workspace_templates(templates_dir: Path, root: Path, created: list, skipped: list) -> None:
    target_dir = root / "_templates"
    for template_name in WORKSPACE_TEMPLATE_FILES:
        source_path = templates_dir / template_name
        target_path = target_dir / template_name
        if target_path.exists():
            skipped.append(str(target_path))
            continue
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(source_path.read_text(encoding="utf-8"), encoding="utf-8")
        created.append(str(target_path))


def main():
    parser = argparse.ArgumentParser(description="初始化学习工作区骨架")
    parser.add_argument("--root", default="./study", help="工作区根目录,默认 ./study")
    parser.add_argument("--topic", required=True, help="学习主题,例如 'RAG 系统原理'")
    parser.add_argument(
        "--domain",
        required=True,
        help=(
            "领域类型,决定资料地图文件名。预设别名: "
            + ", ".join(DOMAIN_READING_MAP.keys())
            + "。其他任意字符串也可以,不在预设里会落到通用命名,"
            "或配合 --reading-map-name/--reading-map-title 自定义。"
        ),
    )
    parser.add_argument(
        "--reading-map-name",
        default=None,
        help="自定义资料地图文件名,覆盖 domain 预设(可选)",
    )
    parser.add_argument(
        "--reading-map-title",
        default=None,
        help="自定义资料地图标题,覆盖 domain 预设(可选)",
    )
    parser.add_argument(
        "--diagnosis-mode",
        default="完整诊断",
        help="诊断方式说明,例如 '完整诊断' 或 '已跳过,按用户自述目标执行'",
    )
    args = parser.parse_args()

    root = Path(args.root)
    skill_dir = get_skill_dir()
    templates_dir = skill_dir / "templates"

    if not templates_dir.exists():
        raise SystemExit(f"找不到模板目录: {templates_dir}")

    preset_filename, preset_title = DOMAIN_READING_MAP.get(
        args.domain, DEFAULT_READING_MAP
    )
    reading_map_filename = args.reading_map_name or preset_filename
    reading_map_title = args.reading_map_title or preset_title
    today = datetime.date.today().isoformat()

    mapping = {
        "TOPIC": args.topic,
        "DATE": today,
        "READING_MAP_NAME": reading_map_filename,
        "READING_MAP_NAME_TITLE": reading_map_title,
        "DIAGNOSIS_MODE": args.diagnosis_mode,
    }

    root.mkdir(parents=True, exist_ok=True)
    for sub in SUBDIRS:
        (root / sub).mkdir(parents=True, exist_ok=True)

    created = []
    skipped = []

    write_initial_state(root, args, reading_map_filename, today, created, skipped)

    for out_name, template_name in FILE_MAP:
        out_path = root / out_name
        if out_path.exists():
            skipped.append(str(out_path))
            continue
        template_text = (templates_dir / template_name).read_text(encoding="utf-8")
        out_path.write_text(render(template_text, mapping), encoding="utf-8")
        created.append(str(out_path))

    # 资料阅读地图(文件名按 domain 决定)
    reading_map_path = root / reading_map_filename
    if reading_map_path.exists():
        skipped.append(str(reading_map_path))
    else:
        template_text = (templates_dir / "READING-MAP.md.template").read_text(encoding="utf-8")
        reading_map_path.write_text(render(template_text, mapping), encoding="utf-8")
        created.append(str(reading_map_path))

    copy_workspace_templates(templates_dir, root, created, skipped)

    print(f"学习工作区已初始化: {root.resolve()}")
    print(f"使用的 Skill 目录: {skill_dir}")
    print(f"\n创建了 {len(created)} 个文件:")
    for f in created:
        print(f"  - {f}")
    if skipped:
        print(f"\n以下文件已存在,跳过(避免覆盖已有内容):")
        for f in skipped:
            print(f"  - {f}")

    print(
        "\n下一步: 结合诊断结果填写 MISSION.md 和 MASTER-PLAN.md, "
        "再展开 COURSE-ROADMAP.md / COURSE-LIST.md / "
        f"{reading_map_filename}, 并运行 validate_workspace.py 做一致性检查。"
    )


if __name__ == "__main__":
    main()
