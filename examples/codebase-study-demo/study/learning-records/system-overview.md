# Learning Record：MiniAgentFlow 系统总览

> 只在用户真正展示理解（Understanding 及以上）后才创建这份文件。

日期：2026-06-25

## 用户已经掌握了什么

用户已经掌握 MiniAgentFlow 的基础项目地图，能够区分核心模块职责，并能复述从 CLI 到状态保存的主链路。

## 掌握等级

- 等级：Understanding
- 判定依据：用户能用自己的话解释模块职责和主链路，并能纠正 Scheduler / Executor 的职责混淆。

## 证据是什么

用户在理解检查中能够说明：

1. CLI 负责命令入口和参数解析。
2. Task 是任务数据对象。
3. Scheduler 负责调度，而不是直接执行工具。
4. Executor 负责执行任务。
5. State Store 负责保存状态和结果。

## 当时的理解检查

- 检查方式：职责边界复述 + 主链路复述。
- 题目：不用看上文，说明 MiniAgentFlow 从用户输入命令到保存任务状态经过哪些核心模块，每个模块负责什么。
- 用户回答摘要：用户正确复述了主链路，并能说出 Scheduler 与 Executor 的区别。
- 是否一次通过：是。
- 纠偏后是否通过：不需要纠偏后再测。

## 仍需注意的边界/误区

1. Tool Registry 还只是听过，尚未达到 Understanding。
2. State Store 的恢复和调试价值还需要在 L03/L07 深入。

## 这会解锁后续什么内容

可以进入 L02，从 CLI 入口追到 Scheduler，开始读具体函数调用链。

## 复习计划

- 是否已加入 `REVIEW-SCHEDULE.md`：是。
- 建议复习方式：主动回忆 + 调用链复述。
