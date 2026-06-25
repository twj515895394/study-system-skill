#!/usr/bin/env python3
"""
初始化一个 study/ 学习工作区骨架。

用法:
    python init_workspace.py --root ./study --topic "RAG 系统原理" --domain code

domain 接受任意字符串。code/course/industry/exam/child 是5个常见预设(决定资料
地图文件名),命中即用对应命名;不在预设里的领域(比如"研究资料阅读""技能训练""产品
体系学习")不会报错——会落到通用命名 RESOURCE-READING-MAP.md,也可以用
--reading-map-name / --reading-map-title 完全自定义文件名和标题。
不要因为某个学习场景"不属于这5类"就为难,这几个预设只是省事的别名,不是穷举。
"""
import argparse
import datetime
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
]


def render(text: str, mapping: dict) -> str:
    for key, value in mapping.items():
        text = text.replace("{{" + key + "}}", value)
    return text


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
    skill_dir = Path(__file__).resolve().parent.parent
    templates_dir = skill_dir / "templates"

    if not templates_dir.exists():
        raise SystemExit(f"找不到模板目录: {templates_dir}")

    preset_filename, preset_title = DOMAIN_READING_MAP.get(
        args.domain, DEFAULT_READING_MAP
    )
    reading_map_filename = args.reading_map_name or preset_filename
    reading_map_title = args.reading_map_title or preset_title

    mapping = {
        "TOPIC": args.topic,
        "DATE": datetime.date.today().isoformat(),
        "READING_MAP_NAME": reading_map_filename,
        "READING_MAP_NAME_TITLE": reading_map_title,
        "DIAGNOSIS_MODE": args.diagnosis_mode,
    }

    root.mkdir(parents=True, exist_ok=True)
    for sub in SUBDIRS:
        (root / sub).mkdir(parents=True, exist_ok=True)

    created = []
    skipped = []

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

    print(f"学习工作区已初始化: {root.resolve()}")
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
        f"{reading_map_filename}"
    )


if __name__ == "__main__":
    main()
