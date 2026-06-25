#!/usr/bin/env python3
"""
生成规范 handoff 文件,并同步 STATE.json / CURRENT.md。

用法:
    python "${CLAUDE_SKILL_DIR}/scripts/add_handoff.py" \
      --root ./study \
      --lesson-id L02 \
      --title "CLI 入口到任务调度的调用链" \
      --status 待理解检查
"""
import argparse
from pathlib import Path

from study_utils import (
    handoff_output_path,
    normalize_lesson_id,
    read_text,
    relative_to_root,
    render_template,
    require_workspace,
    today,
    update_current_file,
    update_state,
    validate_status,
    write_text,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="创建 handoff 并同步当前状态")
    parser.add_argument("--root", default="./study", help="study 工作区根目录")
    parser.add_argument("--lesson-id", required=True, help="课次编号,例如 L02 或 2")
    parser.add_argument("--title", required=True, help="课程标题")
    parser.add_argument("--status", required=True, help="本节课状态")
    parser.add_argument("--date", default=None, help="handoff 日期,默认今天")
    parser.add_argument("--summary", default="", help="可选摘要,会写入 handoff 顶部提示")
    parser.add_argument("--force", action="store_true", help="允许覆盖已存在的 handoff")
    args = parser.parse_args()

    root = Path(args.root)
    require_workspace(root)
    lesson_id = normalize_lesson_id(args.lesson_id)
    validate_status(args.status)

    template_path = root / "_templates" / "handoff.md.template"
    if not template_path.exists():
        raise SystemExit(f"找不到 handoff 模板: {template_path}")

    out_path = handoff_output_path(root, lesson_id, args.title, args.date)
    if out_path.exists() and not args.force:
        raise SystemExit(f"handoff 已存在,如需覆盖请加 --force: {out_path}")

    mapping = {
        "LESSON_NUM": lesson_id,
        "LESSON_TITLE": args.title,
        "DATE": args.date or today(),
    }
    content = render_template(read_text(template_path), mapping)
    if args.summary:
        content = content.replace("## 本节课状态", f"> 摘要：{args.summary}\n\n## 本节课状态")
    content = content.replace("（使用统一状态：进行中 / 待理解检查 / 待补课 / 补课中 / 已完成 / 需复习 / 暂停；必要时补充原因）", args.status)
    write_text(out_path, content)

    rel_handoff_path = relative_to_root(out_path, root)
    update_state(
        root,
        current_lesson_id=lesson_id,
        current_lesson_title=args.title,
        current_status=args.status,
        latest_handoff=rel_handoff_path,
    )
    update_current_file(
        root,
        lesson_id=lesson_id,
        lesson_title=args.title,
        status=args.status,
        latest_handoff=rel_handoff_path,
    )

    print(f"已创建 handoff: {rel_handoff_path}")
    print("已同步 STATE.json / CURRENT.md。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
