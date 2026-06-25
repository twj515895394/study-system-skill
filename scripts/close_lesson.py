#!/usr/bin/env python3
"""
课程收尾脚本: 同步 STATE.json / CURRENT.md / PROGRESS.md / COURSE-LIST.md。

用法:
    python "${CLAUDE_SKILL_DIR}/scripts/close_lesson.py" \
      --root ./study \
      --lesson-id L01 \
      --title "系统总览与核心目录" \
      --status 已完成 \
      --handoff handoffs/2026-06-25-L01-system-overview.md \
      --reference reference/L01-system-overview.md \
      --learning-record learning-records/system-overview.md \
      --next-step "进入 L02《CLI 入口到任务调度的调用链》"
"""
import argparse
from pathlib import Path

from study_utils import (
    normalize_lesson_id,
    require_workspace,
    update_current_file,
    update_markdown_table_row,
    update_state,
    validate_status,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="收尾课程并同步状态文件")
    parser.add_argument("--root", default="./study", help="study 工作区根目录")
    parser.add_argument("--lesson-id", required=True, help="课次编号,例如 L01 或 1")
    parser.add_argument("--title", required=True, help="课程标题")
    parser.add_argument("--status", default="已完成", help="课程最终状态")
    parser.add_argument("--phase", default=None, help="当前阶段,可选")
    parser.add_argument("--handoff", default=None, help="handoff 相对路径")
    parser.add_argument("--reference", default=None, help="reference 相对路径")
    parser.add_argument("--learning-record", default=None, help="learning-record 相对路径")
    parser.add_argument("--next-step", default=None, help="写入 CURRENT.md 的下一步")
    args = parser.parse_args()

    root = Path(args.root)
    require_workspace(root)
    lesson_id = normalize_lesson_id(args.lesson_id)
    validate_status(args.status)

    if args.status != "已完成" and args.learning_record:
        raise SystemExit("只有状态为 已完成 时才允许写入 --learning-record")

    state_updates = {
        "current_lesson_id": lesson_id,
        "current_lesson_title": args.title,
        "current_status": args.status,
    }
    if args.phase is not None:
        state_updates["current_phase"] = args.phase
    if args.handoff:
        state_updates["latest_handoff"] = args.handoff
    update_state(root, **state_updates)

    update_current_file(
        root,
        lesson_id=lesson_id,
        lesson_title=args.title,
        status=args.status,
        latest_handoff=args.handoff,
        next_step=args.next_step,
    )

    progress_updates = {3: args.status}
    if args.handoff:
        progress_updates[5] = f"`{args.handoff}`"
    if args.reference:
        progress_updates[6] = f"`{args.reference}`"
    if args.learning_record:
        progress_updates[7] = f"`{args.learning_record}`"
    progress_changed = update_markdown_table_row(root / "PROGRESS.md", lesson_id, progress_updates)

    course_changed = update_markdown_table_row(root / "COURSE-LIST.md", lesson_id, {3: args.status})

    print("已同步 STATE.json / CURRENT.md。")
    print(f"PROGRESS.md 更新: {'是' if progress_changed else '未找到对应课次'}")
    print(f"COURSE-LIST.md 更新: {'是' if course_changed else '未找到对应课次'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
