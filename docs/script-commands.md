# Script Commands：课程操作脚本

P4 开始，`study-system` 不再只依赖 Agent 手动改多份 Markdown，而是提供一组轻量脚本来减少状态漂移。

这些脚本都默认不创建新的学习计划，只操作已有 `study/` 工作区。

## 命令总览

| 脚本 | 用途 | 主要更新 |
|---|---|---|
| `new_lesson.py` | 基于课型模板创建新课 | `lessons/`、`STATE.json`、`CURRENT.md`、`PROGRESS.md`、`COURSE-LIST.md` |
| `add_handoff.py` | 生成规范 handoff | `handoffs/`、`STATE.json`、`CURRENT.md` |
| `add_learning_record.py` | 创建学习记录并追加复习计划 | `learning-records/`、`REVIEW-SCHEDULE.md` |
| `close_lesson.py` | 课程收尾，同步状态表 | `STATE.json`、`CURRENT.md`、`PROGRESS.md`、`COURSE-LIST.md` |
| `validate_workspace.py` | 校验工作区一致性 | 只读，不改文件 |

## 1. 创建新课

```bash
python "${CLAUDE_SKILL_DIR}/scripts/new_lesson.py" \
  --root ./study \
  --lesson-id L02 \
  --title "CLI 入口到任务调度的调用链" \
  --lesson-type code-trace \
  --phase "Phase 1 - 项目地图与主链路"
```

常用课型：

| lesson-type | 模板 |
|---|---|
| `concept-primer` | 概念入门课 |
| `code-trace` | 源码调用链课 |
| `architecture-walkthrough` | 架构拆解课 |
| `paper-reading` | 论文阅读课 |
| `exercise-review` | 练习/错题复盘课 |
| `implementation-lab` | 动手实现课 |
| `phase-review` | 阶段复盘课 |
| `generic` | 通用课 |

效果：

1. 从 `study/_templates/` 选择对应模板。
2. 创建 `study/lessons/Lxx-title.md`。
3. 把 `STATE.json.current_lesson_*` 更新到当前课程。
4. 更新 `CURRENT.md`。
5. 尝试同步 `PROGRESS.md` / `COURSE-LIST.md` 中对应课次状态。

## 2. 添加 handoff

```bash
python "${CLAUDE_SKILL_DIR}/scripts/add_handoff.py" \
  --root ./study \
  --lesson-id L02 \
  --title "CLI 入口到任务调度的调用链" \
  --status 待理解检查 \
  --summary "本节已讲完主调用链，等待用户复述"
```

效果：

1. 创建 `study/handoffs/YYYY-MM-DD-Lxx-title.md`。
2. 同步 `STATE.json.latest_handoff`。
3. 同步 `CURRENT.md` 的最新 handoff 和当前状态。

## 3. 添加 learning-record

```bash
python "${CLAUDE_SKILL_DIR}/scripts/add_learning_record.py" \
  --root ./study \
  --topic "Scheduler / Executor 职责边界" \
  --lesson-id L01 \
  --mastery Understanding \
  --evidence "用户能说明 Scheduler 负责调度，Executor 负责执行"
```

允许的掌握等级：

```text
Understanding / Skill / Capability
```

效果：

1. 创建 `study/learning-records/<topic-slug>.md`。
2. 在记录中写入来源课次、掌握等级和通过证据。
3. 默认追加一行到 `REVIEW-SCHEDULE.md`。

如果不想追加复习计划：

```bash
python "${CLAUDE_SKILL_DIR}/scripts/add_learning_record.py" \
  --root ./study \
  --topic "Scheduler / Executor 职责边界" \
  --lesson-id L01 \
  --mastery Understanding \
  --evidence "用户能说明二者边界" \
  --skip-review
```

## 4. 收尾课程

```bash
python "${CLAUDE_SKILL_DIR}/scripts/close_lesson.py" \
  --root ./study \
  --lesson-id L01 \
  --title "系统总览与核心目录" \
  --status 已完成 \
  --handoff handoffs/2026-06-25-L01-system-overview.md \
  --reference reference/L01-system-overview.md \
  --learning-record learning-records/system-overview.md \
  --next-step "进入 L02《CLI 入口到任务调度的调用链》"
```

效果：

1. 同步 `STATE.json.current_status`。
2. 同步 `CURRENT.md`。
3. 更新 `PROGRESS.md` 中对应课次的状态、handoff、reference、learning-record。
4. 更新 `COURSE-LIST.md` 中对应课次的状态。

注意：如果 `--status` 不是 `已完成`，脚本会拒绝写入 `--learning-record`。

## 5. 校验工作区

```bash
python "${CLAUDE_SKILL_DIR}/scripts/validate_workspace.py" --root ./study
```

建议在这些时机运行：

1. 初始化完成后。
2. 每节课收尾后。
3. 新会话接手时。
4. 发现 `STATE.json`、`CURRENT.md`、`PROGRESS.md` 状态不一致时。

## 推荐操作流

```bash
# 1. 创建新课
python "${CLAUDE_SKILL_DIR}/scripts/new_lesson.py" \
  --root ./study \
  --lesson-id L02 \
  --title "CLI 入口到任务调度的调用链" \
  --lesson-type code-trace

# 2. 上课、理解检查
# 由 Agent 和用户在对话中完成

# 3. 生成 handoff
python "${CLAUDE_SKILL_DIR}/scripts/add_handoff.py" \
  --root ./study \
  --lesson-id L02 \
  --title "CLI 入口到任务调度的调用链" \
  --status 已完成

# 4. 写学习记录
python "${CLAUDE_SKILL_DIR}/scripts/add_learning_record.py" \
  --root ./study \
  --topic "CLI 到 Scheduler 调用链" \
  --lesson-id L02 \
  --mastery Understanding \
  --evidence "用户能复述入口、任务创建和调度提交过程"

# 5. 收尾同步状态
python "${CLAUDE_SKILL_DIR}/scripts/close_lesson.py" \
  --root ./study \
  --lesson-id L02 \
  --title "CLI 入口到任务调度的调用链" \
  --status 已完成

# 6. 校验
python "${CLAUDE_SKILL_DIR}/scripts/validate_workspace.py" --root ./study
```

## 设计边界

这些脚本只做轻量同步，不替代 Agent 的教学判断。

脚本负责：

- 创建文件。
- 渲染模板。
- 更新状态字段。
- 降低多文件状态漂移。

Agent 仍然负责：

- 诊断用户基础。
- 设计课程内容。
- 判断理解检查是否通过。
- 决定是否补课或复习。
- 写出高质量讲解和 handoff 内容。
