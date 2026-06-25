# 学习状态模型

本文件定义 `STATE.json`、`CURRENT.md`、`PROGRESS.md`、`COURSE-LIST.md`、`handoffs/` 中统一使用的状态枚举，避免不同文件对同一课程状态使用不同词。

## 标准状态枚举

| 状态 | 含义 | 什么时候使用 |
|---|---|---|
| 未开始 | 课程已规划，但尚未进入 | 初始化课程清单或后续排课时 |
| 进行中 | 正在讲解、练习或讨论 | 本节课尚未进入正式理解检查 |
| 待理解检查 | 内容已讲完，等待用户完成理解检查 | 不能直接进入下一课 |
| 待补课 | 理解检查暴露出前置断层，需要插入补课 | 需要按动态补课规则处理 |
| 补课中 | 正在执行补课/概念复习/源码小课 | 补课结束后必须回到主线 |
| 已完成 | 理解检查通过，课程已收尾 | 可以进入下一课 |
| 需复习 | 课程曾通过，但后续发现遗忘或迁移失败 | 应安排复习或阶段回顾 |
| 暂停 | 用户主动暂停，或外部资料/目标未确认 | 继续前需要先恢复上下文或补资料 |

## STATE.json 字段

`STATE.json` 是机器可读的状态摘要，不替代 Markdown 文件，但用于快速校验和跨 Agent 续接。

| 字段 | 含义 |
|---|---|
| `schema_version` | 状态文件结构版本 |
| `topic` | 学习主题 |
| `domain` | 学习领域，用于资料地图命名和诊断问题选择 |
| `reading_map` | 当前工作区的资料地图文件名 |
| `diagnosis_mode` | 诊断方式说明 |
| `current_lesson_id` | 当前课次编号，例如 `1` 或 `L01` |
| `current_lesson_title` | 当前课程标题 |
| `current_phase` | 当前阶段 |
| `current_status` | 当前状态，必须使用标准状态枚举 |
| `latest_handoff` | 最新 handoff 的相对路径，例如 `handoffs/2026-06-25-L01-intro.md` |
| `blocked_by` | 阻塞项列表 |
| `makeup_count_in_current_phase` | 当前阶段内连续/累计补课次数，用于发现补课失控 |
| `last_updated` | 最后更新时间，YYYY-MM-DD |

## 使用约束

1. `STATE.json.current_status`、`CURRENT.md`、`PROGRESS.md`、`COURSE-LIST.md`、最新 handoff 的状态必须一致。
2. `CURRENT.md` 只能有一个当前状态。
3. `PROGRESS.md` 与 `COURSE-LIST.md` 的同一课次状态必须一致。
4. handoff 的“本节课状态”必须使用上表状态之一，必要时可在状态后补充原因。
5. 只有状态为 `已完成`，才允许把对应内容写入 `learning-records/` 和 `GLOSSARY.md`。
6. 状态为 `待理解检查`、`待补课`、`补课中` 时，不允许直接跳到下一节主线课。
7. 连续两次以上进入 `待补课` / `补课中` 且未回到主线时，必须提醒用户重新校准主计划或决定是否先回主线。

## 校验命令

```bash
python "${CLAUDE_SKILL_DIR}/scripts/validate_workspace.py" --root ./study
```

校验脚本只读不写，用来发现缺失文件、状态枚举错误、`STATE.json` 与 Markdown 文件冲突、`PROGRESS.md` / `COURSE-LIST.md` 状态不一致等问题。
