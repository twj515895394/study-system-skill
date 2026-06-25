# Handoff：第 L01 课 —— 系统总览与核心目录

日期：2026-06-25

## 本节课状态

已完成。

## 本节课目标

建立 MiniAgentFlow 的项目地图，理解核心模块职责，并为下一节源码调用链课做准备。

## 实际学习内容

1. 梳理了项目的主要目录：`cli/`、`core/`、`tools/`、`state/`、`config/`。
2. 用 Mermaid 画出了 CLI -> Task -> Scheduler -> Executor -> State Store 的主链路。
3. 区分了 Scheduler 和 Executor 的职责边界。

## 已确认理解

用户通过职责边界复述和主链路复述证明：

- 能说明 CLI、Task、Scheduler、Executor、State Store 各自负责什么。
- 能解释为什么 Scheduler 不是直接执行工具的模块。
- 能说明下一节为什么要从 CLI 入口追到 Scheduler。

## 已纠正的问题

用户一开始把 Scheduler 理解成“执行器”，已纠正为：Scheduler 负责调度策略，Executor 负责实际执行。

## 资料/源码阅读进度

已建立阅读地图，但尚未深入具体函数。下一节从 `src/miniflow/cli.py` 开始追踪。

## 练习进度

完成了模块职责复述练习。未进行代码修改练习。

## 文档更新情况

已更新：

- `STATE.json`
- `CURRENT.md`
- `PROGRESS.md`
- `COURSE-LIST.md`
- `reference/L01-system-overview.md`
- `learning-records/system-overview.md`
- `GLOSSARY.md`
- `REVIEW-SCHEDULE.md`

## 下节课计划

L02：《CLI 入口到任务调度的调用链》。建议使用 `code-trace.md.template`。

## 新会话续接提示

1. 先读取 `STATE.json`、`CURRENT.md`、本 handoff。
2. 直接告诉用户：L01 已完成，下一节开始追 `src/miniflow/cli.py` 到 `src/miniflow/core/scheduler.py` 的调用链。
3. 不需要重新问“我们学到哪了”。
