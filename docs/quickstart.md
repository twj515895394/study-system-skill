# Quickstart：5 分钟跑通 study-system

这份指南帮助你快速理解 `study-system` 怎么用，以及初始化后的 `study/` 工作区应该如何维护。

## 1. 安装 Skill

### 全局安装

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/twj515895394/study-system-skill \
  ~/.claude/skills/study-system
```

### 项目级安装

```bash
mkdir -p .claude/skills
git clone https://github.com/twj515895394/study-system-skill \
  .claude/skills/study-system
```

## 2. 触发 Skill

在 Claude Code 或其他支持 Skill 的 Agent 里说：

```text
帮我系统学习这个仓库，建立 study 学习工作区。
```

也可以更具体：

```text
我要系统读懂这个项目的源码，目标是能二开一个小功能。
```

## 3. 初始化工作区

Skill 会引导 Agent 运行：

```bash
python "${CLAUDE_SKILL_DIR}/scripts/init_workspace.py" \
  --root ./study \
  --topic "你的学习主题" \
  --domain code
```

常见 `domain`：

| domain | 场景 | 生成的资料地图 |
|---|---|---|
| `code` | 源码项目 | `SOURCE-READING-MAP.md` |
| `course` | 教材/课程 | `TEXTBOOK-READING-MAP.md` |
| `industry` | 行业/资料包 | `RESOURCE-READING-MAP.md` |
| `exam` | 备考 | `EXAM-ROADMAP.md` |
| `child` | 孩子学科同步 | `SCHOOL-SYNC-PLAN.md` |

## 4. 填主计划

初始化只是生成骨架。接下来要填：

1. `MISSION.md`：为什么学、学到什么程度、暂不学什么。
2. `MASTER-PLAN.md`：阶段路线、课程清单、阶段验收。
3. `COURSE-ROADMAP.md` / `COURSE-LIST.md`：主计划的展开视图。
4. 资料地图：按学习顺序排资料或源码，而不是机械列目录。

## 5. 上第一课

每节课前先选课型：

| 课型 | 模板 |
|---|---|
| 概念入门课 | `study/_templates/lesson-types/concept-primer.md.template` |
| 源码调用链课 | `study/_templates/lesson-types/code-trace.md.template` |
| 架构拆解课 | `study/_templates/lesson-types/architecture-walkthrough.md.template` |
| 论文阅读课 | `study/_templates/lesson-types/paper-reading.md.template` |
| 练习复盘课 | `study/_templates/lesson-types/exercise-review.md.template` |
| 动手实现课 | `study/_templates/lesson-types/implementation-lab.md.template` |
| 阶段复盘课 | `study/_templates/lesson-types/phase-review.md.template` |

## 6. 做理解检查

默认最低通过线是 `Understanding`。

| 等级 | 名称 | 是否允许推进 |
|---|---|---|
| 0 | Not Started | 否 |
| 1 | Exposure | 否 |
| 2 | Understanding | 是 |
| 3 | Skill | 是 |
| 4 | Capability | 是 |

用户只说“懂了”不算通过，必须能复述、对照、画流程、判断边界、做小设计或改错。

## 7. 收尾并校验

每节课结束至少更新：

- `STATE.json`
- `CURRENT.md`
- `PROGRESS.md`
- `handoffs/`
- `reference/`

只有理解检查通过，才更新：

- `learning-records/`
- `GLOSSARY.md`
- `REVIEW-SCHEDULE.md`

然后运行：

```bash
python "${CLAUDE_SKILL_DIR}/scripts/validate_workspace.py" --root ./study
```

## 8. 看完整示例

完整示例见：

```text
examples/codebase-study-demo/
```

建议从 `examples/codebase-study-demo/README.md` 开始看。
