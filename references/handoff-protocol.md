# 跨会话衔接协议

这是这套方法论真正的威力所在：换一个会话，不用从头问“我们之前学到哪了”。但前提是每节课结束都老老实实更新文件，新会话开始都老老实实按顺序读。

## 新会话进入已有学习项目时，按这个顺序读

1. `README.md` —— 这个工作区是什么、目录结构
2. `STATE.json` —— 机器可读状态摘要，快速确认当前课次、状态、最新 handoff
3. `MASTER-PLAN.md` —— 唯一权威主计划，所有其他文件的依据
4. `MISSION.md` —— 为什么学，避免推进方向跑偏
5. `TEACHING-PROTOCOL.md` —— 教学风格与偏好协议，确保不同会话间上课节奏、讲解风格和偏好高度一致
6. `CURRENT.md` —— 当前学习状态，人类可读版
7. `PROGRESS.md` —— 所有课程的整体进度看板
8. 最新一份 `handoffs/` —— 上节课具体发生了什么
9. 必要时读 `reference/`、`learning-records/`、`QUESTION-PARKING-LOT.md`、`REVIEW-SCHEDULE.md`、`NOTES.md`

不需要每份都通读全文，`STATE.json`、`CURRENT.md`、`TEACHING-PROTOCOL.md` 和最新 handoff 通常已经够接上当前上下文；`MASTER-PLAN.md` 和 `MISSION.md` 主要用来校验“接下来要做的事和主线方向是否一致”。

## 每节课结束必须更新

- `STATE.json`
- `PROGRESS.md`
- `CURRENT.md`
- 一份新的 `handoffs/`
- 对应的 `reference/`（课程精华压缩版，不是课堂讲义）

## 第一节课结束前或风格偏好变动时更新

- `TEACHING-PROTOCOL.md`（第一节课结束前，必须与用户对齐并初始化该协议；后续上课若发现节奏/偏好有变，须同步更新）

## 只有通过理解检查后才更新

- `learning-records/`（记录用户已经掌握了什么、证据是什么、解锁了后续什么内容）
- `GLOSSARY.md`（术语真正理解后才写入）
- `REVIEW-SCHEDULE.md`（把关键知识点加入复习计划，用主动回忆/迁移题检查长期掌握）

## 用户偏好变化时更新

- `NOTES.md`（作为临时笔记和备忘，成熟的偏好应整理进 `TEACHING-PROTOCOL.md`）

## 旁支问题处理

不阻塞当前课程理解的问题先写入 `QUESTION-PARKING-LOT.md`，不要立刻打断主线。只有当问题会影响理解检查或后续课程时，才转为“待补课”。

## handoff 命名规范

建议使用：

```text
handoffs/YYYY-MM-DD-Lxx-short-slug.md
```

示例：

```text
handoffs/2026-06-25-L01-system-overview.md
```

这样新会话和校验脚本都能稳定定位最新交接单。

## handoff 应该写什么

handoff 不是流水账，是“如果换一个完全没有上下文的会话接手，看这一份文件应该能立刻知道该做什么”。至少包含：本节课状态、本节课目标、实际学习内容、已确认理解、已纠正的问题、资料/源码阅读进度、练习进度、文档更新情况、下节课计划、新会话续接提示。

## 状态一致性要求

`STATE.json`、`CURRENT.md`、`PROGRESS.md`、`COURSE-LIST.md`、最新 handoff 必须使用统一状态模型，状态取值见 `references/status-model.md`。

关键约束：

1. 如果当前状态是 `待理解检查`、`待补课` 或 `补课中`，不要直接进入下一课。
2. 只有状态为 `已完成`，才允许写入 `learning-records/`、`GLOSSARY.md`、`REVIEW-SCHEDULE.md`。
3. 如果最新 handoff 与 `STATE.json` / `CURRENT.md` / `PROGRESS.md` 状态冲突，优先停下来同步状态，而不是继续授课。
4. 阶段收尾、新会话接手、或发现状态冲突时，运行：

```bash
python "${CLAUDE_SKILL_DIR}/scripts/validate_workspace.py" --root ./study
```
