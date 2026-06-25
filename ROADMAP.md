# ROADMAP

## 当前定位

`study-system` 的目标不是生成一份一次性学习计划，而是提供一套可长期运行、可跨会话续接、可校验状态的 AI 伴学工作区方法。

## 已完成

### P0 - 基础可用性

- 支持 `CLAUDE_SKILL_DIR` 调用初始化脚本。
- 补齐 Claude Code 安装说明。
- 统一课程状态枚举。
- 修复未渲染模板占位符。
- 补齐 MIT License。

### P1 - 工作区运行时可靠性

- 新增 `STATE.json`。
- 新增 `validate_workspace.py`。
- 初始化时生成 `QUESTION-PARKING-LOT.md` 和 `REVIEW-SCHEDULE.md`。
- 初始化时复制核心模板到 `study/_templates/`。
- 增加 handoff 命名规范。

### P2 - 学习效果增强

- 新增理解检查 Rubric。
- 新增多课型模板：概念入门、源码调用链、架构拆解、论文阅读、练习复盘、动手实现、阶段复盘。
- 新增复习测验模板。
- 升级 lesson / learning-record 模板，要求记录掌握等级和证据。

### P3 - 开源传播与示例

- 新增 `examples/codebase-study-demo/`。
- 新增 Quickstart 文档。
- 新增 ROADMAP / CHANGELOG。

### P4 - 脚本化课程操作

- 新增 `scripts/study_utils.py`，复用状态、模板、slug、Markdown section/table 更新等逻辑。
- 新增 `scripts/new_lesson.py`：基于课型模板创建新课程，并同步 `STATE.json` / `CURRENT.md`。
- 新增 `scripts/add_handoff.py`：生成规范 handoff，并同步 latest handoff。
- 新增 `scripts/add_learning_record.py`：写入学习记录，并可追加 `REVIEW-SCHEDULE.md`。
- 新增 `scripts/close_lesson.py`：课程收尾时同步 `STATE.json`、`CURRENT.md`、`PROGRESS.md`、`COURSE-LIST.md`。
- 新增 `docs/script-commands.md`，说明完整命令用法。

## 下一步建议

### P5 - 测试与 CI

目标：让模板和脚本有最小工程保障。

计划：

- 增加 `tests/test_init_workspace.py`。
- 增加 `tests/test_validate_workspace.py`。
- 增加 `tests/test_script_commands.py`。
- 增加 GitHub Actions，至少跑初始化、课程创建、课程收尾和校验脚本。

### P6 - 更多真实示例

计划示例：

- `examples/course-study-demo/`：课程/教材学习。
- `examples/paper-reading-demo/`：论文组阅读。
- `examples/exam-prep-demo/`：备考规划。
- `examples/child-learning-demo/`：孩子学科同步。

### P7 - UI / Agent 协作扩展

长期方向：

- 把 `study/` 工作区接入可视化 UI。
- 展示当前课程、进度、问题停车场、复习计划。
- 支持 Agent 在 UI 中推进课程、生成 handoff、执行状态校验。
