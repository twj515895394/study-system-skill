# MiniAgentFlow 源码学习 工作区

这是一个持续推进的学习工作区，用于系统学习虚构项目「MiniAgentFlow」。

## 新会话从这里开始

按顺序读：

1. `STATE.json` —— 当前机器可读状态。
2. `MASTER-PLAN.md` —— 唯一权威主计划。
3. `MISSION.md` —— 为什么学。
4. `TEACHING-PROTOCOL.md` —— 教学风格和理解检查偏好。
5. `CURRENT.md` —— 当前状态和下一步。
6. `PROGRESS.md` —— 整体进度。
7. `handoffs/2026-06-25-L01-system-overview.md` —— 最新交接。

## 当前状态

第 1 课《系统总览与核心目录》已完成。下一节建议进入第 2 课《CLI 入口到任务调度的调用链》。

## 状态取值

未开始 / 进行中 / 待理解检查 / 待补课 / 补课中 / 已完成 / 需复习 / 暂停

## 校验命令

```bash
python "${CLAUDE_SKILL_DIR}/scripts/validate_workspace.py" --root ./study
```
