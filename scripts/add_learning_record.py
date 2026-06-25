#!/usr/bin/env python3
"""
创建 learning-record,并可追加 REVIEW-SCHEDULE.md。

用法:
    python "${CLAUDE_SKILL_DIR}/scripts/add_learning_record.py" \
      --root ./study \
      --topic "Scheduler / Executor 职责边界" \
      --lesson-id L01 \
      --mastery Understanding \
      --evidence "用户能说明 Scheduler 负责调度, Executor 负责执行"
"""
import argparse
from pathlib import Path

from study_utils import (
    append_review_schedule_row,
    learning_record_output_path,
    normalize_lesson_id,
    read_text,
    relative_to_root,
    render_template,
    require_workspace,
    today,
    validate_mastery_level,
    write_text,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="创建学习记录并同步复习计划")
    parser.add_argument("--root", default="./study", help="study 工作区根目录")
    parser.add_argument("--topic", required=True, help="学习记录主题/概念")
    parser.add_argument("--lesson-id", required=True, help="来源课次,例如 L01 或 1")
    parser.add_argument("--mastery", required=True, help="掌握等级: Understanding / Skill / Capability")
    parser.add_argument("--evidence", required=True, help="通过证据摘要")
    parser.add_argument("--slug", default=None, help="输出文件 slug,默认由 topic 生成")
    parser.add_argument("--first-review", default="", help="第一次复习日期,可选")
    parser.add_argument("--second-review", default="", help="第二次复习日期,可选")
    parser.add_argument("--skip-review", action="store_true", help="不写入 REVIEW-SCHEDULE.md")
    parser.add_argument("--force", action="store_true", help="允许覆盖已存在 learning-record")
    args = parser.parse_args()

    root = Path(args.root)
    require_workspace(root)
    lesson_id = normalize_lesson_id(args.lesson_id)
    validate_mastery_level(args.mastery)

    template_path = root / "_templates" / "learning-record.md.template"
    if not template_path.exists():
        raise SystemExit(f"找不到 learning-record 模板: {template_path}")

    out_path = learning_record_output_path(root, args.topic, args.slug)
    if out_path.exists() and not args.force:
        raise SystemExit(f"learning-record 已存在,如需覆盖请加 --force: {out_path}")

    mapping = {
        "TOPIC_OR_CONCEPT": args.topic,
        "DATE": today(),
    }
    content = render_template(read_text(template_path), mapping)
    content += (
        "\n---\n\n"
        "## 脚本生成摘要\n\n"
        f"- 来源课次：{lesson_id}\n"
        f"- 掌握等级：{args.mastery}\n"
        f"- 通过证据：{args.evidence}\n"
    )
    write_text(out_path, content)

    if not args.skip_review:
        append_review_schedule_row(
            root,
            topic=args.topic,
            lesson_id=lesson_id,
            evidence=args.evidence,
            first_review=args.first_review,
            second_review=args.second_review,
        )

    rel_path = relative_to_root(out_path, root)
    print(f"已创建 learning-record: {rel_path}")
    if not args.skip_review:
        print("已追加 REVIEW-SCHEDULE.md。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
