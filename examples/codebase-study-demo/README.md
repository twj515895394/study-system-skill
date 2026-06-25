# Codebase Study Demo

这是一个“系统学习源码项目”的示例工作区。

目标不是分析某个真实项目，而是展示 `study-system` 生成和维护 `study/` 目录时，文件之间应该如何协作：

- `STATE.json`：机器可读当前状态。
- `MISSION.md` / `MASTER-PLAN.md`：为什么学、怎么学。
- `CURRENT.md` / `PROGRESS.md` / `COURSE-LIST.md`：当前状态和整体进度。
- `SOURCE-READING-MAP.md`：源码阅读路径。
- `lessons/`：具体课程内容。
- `handoffs/`：跨会话续接文档。
- `learning-records/`：只有通过理解检查后才写入的掌握证据。
- `QUESTION-PARKING-LOT.md`：暂不打断主线的问题。
- `REVIEW-SCHEDULE.md`：复习和长期掌握跟踪。

## 示例当前状态

这个 demo 假设用户正在学习一个虚构的任务编排项目 `MiniAgentFlow`。

当前状态：第 1 课《系统总览与核心目录》已完成，下一步准备进入第 2 课《CLI 入口到任务调度的调用链》。

## 推荐阅读顺序

1. `study/STATE.json`
2. `study/CURRENT.md`
3. `study/MASTER-PLAN.md`
4. `study/PROGRESS.md`
5. `study/lessons/L01-system-overview.md`
6. `study/handoffs/2026-06-25-L01-system-overview.md`
7. `study/learning-records/system-overview.md`
