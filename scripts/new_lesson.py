#!/usr/bin/env python3
"""
基于课型模板创建一节新课,并同步 STATE.json / CURRENT.md。

用法:
    python "${CLAUDE_SKILL_DIR}/scripts/new_lesson.py" \
      --root ./study \
      --lesson-id L02 \
      --title "CLI 入口到任务调度的调用链" \
      --lesson-type code-trace \
      --phase "Phase 1 - 项目地图与主链路"
"""
import argparse
from pathlib import Path

from study_utils import (
    LESSON_TYPE_TEMPLATES,
    lesson_output_path,
    lesson_template_path,
    normalize_lesson_id,
    read_text,
    relative_to_root,
    render_template,
    require_workspace,
    today,
    update_current_file,
    update_markdown_table_row,
    update_state,
    validate_status,
    write_text,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="创建一节新课并同步当前状态")
    parser.add_argument("--root", default="./study", help="study 工作区根目录")
    parser.add_argument("--lesson-id", required=True, help="课次编号,例如 L02 或 2")
    parser.add_argument("--title", required=True, help="课程标题")
    parser.add_argument(
        "--lesson-type",
        default="generic",
        choices=sorted(LESSON_TYPE_TEMPLATES.keys()),
        help="课型,用于选择 _templates/lesson-types/ 下的模板",
    )
    parser.add_argument("--phase", default="", help="所属阶段")
    parser.add_argument("--status", default="进行中", help="创建后的课程状态")
    parser.add_argument("--force", action="store_true", help="允许覆盖已存在的课程文件")
    args = parser.parse_args()

    root = Path(args.root)
    require_workspace(root)
    lesson_id = normalize_lesson_id(args.lesson_id)
    validate_status(args.status)

    template_path = lesson_template_path(root, args.lesson_type)
    out_path = lesson_output_path(root, lesson_id, args.title)
    if out_path.exists() and not args.force:
        raise SystemExit(f"课程文件已存在,如需覆盖请加 --force: {out_path}")

    mapping = {
        "LESSON_NUM": lesson_id,
        "LESSON_TITLE": args.title,
        "PHASE_NAME": args.phase,
        "DATE": today(),
        "TOPIC_OR_SCOPE": args.title,
        "TOPIC_OR_CONCEPT": args.title,
    }
    content = render_template(read_text(template_path), mapping)
    write_text(out_path, content)

    rel_lesson_path = relative_to_root(out_path, root)
    update_state(
        root,
        current_lesson_id=lesson_id,
        current_lesson_title=args.title,
        current_phase=args.phase or None,
        current_status=args.status,
    )
    update_current_file(
        root,
        lesson_id=lesson_id,
        lesson_title=args.title,
        status=args.status,
        next_step=f"继续推进 {lesson_id}《{args.title}》。课程文件：`{rel_lesson_path}`。",
    )

    update_markdown_table_row(root / "PROGRESS.md", lesson_id, {3: args.status})
    update_markdown_table_row(root / "COURSE-LIST.md", lesson_id, {3: args.status})

    print(f"已创建课程: {rel_lesson_path}")
    print(f"课型模板: {template_path.relative_to(root).as_posix()}")
    print("已同步 STATE.json / CURRENT.md, 并尝试同步 PROGRESS.md / COURSE-LIST.md。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
