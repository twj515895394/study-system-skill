# Study System - AI 伴学系统自定义 Skill

`study-system` 是一个专为 AI Agent（如 Claude Code、Claude、Gemini 等）设计的**持续伴学系统 Skill**。它将传统的“一问一答式教学”转变为“持续推进的学习工作区运营”，帮助用户在 AI 的协助下，系统化、有步骤、有反馈地吃透任何一个复杂的知识领域或项目。

---

## 🚀 解决的痛点

在传统的 AI 教学/伴学场景中，通常存在以下三个痛点：

1. **缺乏主线**：走到哪讲到哪，学习进度容易失控或跑偏。
2. **没有验收标准**：AI 讲完了不等于用户学会了。缺乏有效的主动理解检查。
3. **跨会话上下文丢失**：新开一个 Chat 窗口，之前学到哪里、掌握到什么程度全部丢失，需要重新对齐。

`study-system` 通过在用户项目根目录下构建一个**持久化、可追踪的学习工作区 (`study/` 目录)**，让 AI 能够像教练一样，跨会话地追踪用户的学习进度、进行理解检查，并动态插入补课计划。

---

## ⚡ 快速入口

- 快速上手：[`docs/quickstart.md`](docs/quickstart.md)
- 完整示例：[`examples/codebase-study-demo/`](examples/codebase-study-demo/)
- 路线图：[`ROADMAP.md`](ROADMAP.md)
- 变更记录：[`CHANGELOG.md`](CHANGELOG.md)

---

## 🧠 核心设计原则

1. **先建体系，再上课程**：不盲目开讲。在正式开始学习前，必须先理清学习目标（Mission）、主计划（Master Plan）和起点，搭建结构化的骨架。
2. **主线固定，动态补课**：学习主线保持清晰，允许因基础薄弱随时插入“补课”或“概念复习”，但补课必须有明确的目的和边界，且结束后必须回到主线。
3. **按掌握程度推进，不按时间推进**：摒弃机械的“X天计划”，只有在用户通过“理解检查”后，才能进入下一课。
4. **“讲过”不等于“学会了”**：严格区分 Exposure、Understanding、Skill、Capability。只有用户能展示 Understanding 及以上，才能将知识记录在学习档案中。
5. **状态一致**：`STATE.json`、`CURRENT.md`、`PROGRESS.md`、`COURSE-LIST.md` 和最新 handoff 必须使用同一套状态模型，避免长期学习过程中状态漂移。
6. **问题不等于补课**：不阻塞主线的问题进入 `QUESTION-PARKING-LOT.md`，避免每个旁支问题都打断课程。
7. **通过不等于长期掌握**：通过理解检查后，还要进入 `REVIEW-SCHEDULE.md` 做后续复习与迁移验证。
8. **先选课型，再写课程**：概念课、源码课、架构课、论文课、练习课、实现课和阶段复盘课使用不同模板。

---

## 📂 项目目录结构

```text
study-system/
├── SKILL.md
├── README.md
├── docs/
│   └── quickstart.md
├── examples/
│   └── codebase-study-demo/
├── scripts/
│   ├── init_workspace.py
│   └── validate_workspace.py
├── references/
│   ├── diagnostic-questions.md
│   ├── lesson-flow.md
│   ├── comprehension-rubric.md
│   ├── dynamic-makeup-rules.md
│   ├── handoff-protocol.md
│   └── status-model.md
└── templates/
    ├── MASTER-PLAN.md.template
    ├── MISSION.md.template
    ├── CURRENT.md.template
    ├── PROGRESS.md.template
    ├── QUESTION-PARKING-LOT.md.template
    ├── REVIEW-SCHEDULE.md.template
    ├── review-quiz.md.template
    └── lesson-types/
        ├── concept-primer.md.template
        ├── code-trace.md.template
        ├── architecture-walkthrough.md.template
        ├── paper-reading.md.template
        ├── exercise-review.md.template
        ├── implementation-lab.md.template
        └── phase-review.md.template
```

---

## 🛠️ 安装方式

### 方式一：Claude Code 全局安装

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/twj515895394/study-system-skill \
  ~/.claude/skills/study-system
```

### 方式二：Claude Code 项目级安装

```bash
mkdir -p .claude/skills
git clone https://github.com/twj515895394/study-system-skill \
  .claude/skills/study-system
```

### 触发方式

安装后，可以直接对 Agent 说：

- “帮我系统学习这个仓库”
- “为这个项目建立 study 学习工作区”
- “我要读懂这个项目/课程/资料”
- “继续上次的 study-system 学习”
- “陪我长期学 X”

---

## 🚦 初始化学习工作区

安装为 Claude Code Skill 后，推荐使用以下命令：

```bash
python "${CLAUDE_SKILL_DIR}/scripts/init_workspace.py" \
  --root ./study \
  --topic "RAG 系统原理" \
  --domain code
```

如果你是在本仓库根目录内本地开发，也可以直接执行：

```bash
python scripts/init_workspace.py --root ./study --topic "RAG 系统原理" --domain code
```

初始化会生成：

- `STATE.json`：机器可读状态摘要。
- `MISSION.md` / `MASTER-PLAN.md` / `CURRENT.md` / `PROGRESS.md` 等核心看板。
- `QUESTION-PARKING-LOT.md`：问题停车场，用于控制发散。
- `REVIEW-SCHEDULE.md`：复习计划，用于跟踪长期掌握。
- `study/_templates/`：工作区内置课程、handoff、learning-record、review quiz 和多课型模板。

### 参数说明

- `--root`: 工作区根目录，默认 `./study`。
- `--topic`: 学习主题名称。
- `--domain`: 学习领域，决定生成的资料地图文件名。
  - `code` -> `SOURCE-READING-MAP.md` (源码阅读地图)
  - `course` -> `TEXTBOOK-READING-MAP.md` (教材阅读地图)
  - `industry` -> `RESOURCE-READING-MAP.md` (资料阅读地图)
  - `exam` -> `EXAM-ROADMAP.md` (考试路线图)
  - `child` -> `SCHOOL-SYNC-PLAN.md` (学校同步进度图)
  - 亦可传入其他自定义字符串，如 `research`。
- `--reading-map-name`: 自定义资料地图文件名（覆盖 domain 默认）。
- `--reading-map-title`: 自定义资料地图标题。
- `--diagnosis-mode`: 诊断模式说明。

---

## 🔄 标准工作流 (The 8-Step Workflow)

```mermaid
graph TD
    A[Step 1: 确认资料与目标] --> B[Step 2: 轻量诊断/确认基础]
    B --> C[Step 3: 运行脚本初始化 study/ 骨架]
    C --> D[Step 4: 填充 MISSION.md 与 MASTER-PLAN.md]
    D --> E[Step 5: 单课循环 - 先选课型再教学]
    E -->|旁支问题| Q[写入 QUESTION-PARKING-LOT.md]
    Q --> E
    E -->|未通过| F[动态判定: 插入补课并回溯]
    F --> E
    E -->|通过| G[Step 6: 更新 STATE/CURRENT/PROGRESS 与 handoff]
    G --> R[写入 learning-records 与 REVIEW-SCHEDULE]
    R --> H[Step 7: 跨会话续接 - 优先读取 STATE/CURRENT/handoff]
    H --> V[Step 8: validate_workspace.py 状态校验]
    V --> E
```

### 详细步骤说明

1. **确认资料与目标 (Step 1)**：AI 明确用户的资料来源（代码、教材、论文等）以及期望达到的终点状态。
2. **轻量诊断 (Step 2)**：AI 从 `references/diagnostic-questions.md` 选取 3-5 个针对性问题，摸清用户基础，制定合适坡度。
3. **搭建工作区 (Step 3)**：AI 调用脚本，在项目目录下生成 `study/` 目录、状态文件、核心看板、问题停车场、复习计划和工作区模板。
4. **填充主计划 (Step 4)**：AI 细化填充 `MASTER-PLAN.md`（课程清单与阶段验收标准）和 `MISSION.md`（定义阶段成功图景）。
5. **单课循环 (Step 5)**：先选择课型模板，再进行“一课一主题”的教学和理解检查。
6. **收尾与记录 (Step 6)**：只有通过检查，才能更新 `STATE.json`、`PROGRESS.md`、`CURRENT.md`、`learning-records/`、`GLOSSARY.md`、`REVIEW-SCHEDULE.md`，并在 `handoffs/` 下写交接单。
7. **跨会话续接 (Step 7)**：新对话开始时，AI 优先读取 `STATE.json`、`CURRENT.md` 和最新 `handoff` 快速热启动。
8. **状态校验 (Step 8)**：阶段收尾、新会话接手、或发现状态冲突时运行 `validate_workspace.py`。

---

## 🧩 课型模板

| 课型 | 适用场景 | 模板 |
|---|---|---|
| 概念入门课 | 第一次接触核心概念 | `lesson-types/concept-primer.md.template` |
| 源码调用链课 | 读懂具体 API/CLI/UI 调用路径 | `lesson-types/code-trace.md.template` |
| 架构拆解课 | 理解模块职责、组件关系、设计取舍 | `lesson-types/architecture-walkthrough.md.template` |
| 论文阅读课 | 读懂论文问题、方法、实验、局限 | `lesson-types/paper-reading.md.template` |
| 练习/错题复盘课 | 暴露误区并做迁移 | `lesson-types/exercise-review.md.template` |
| 动手实现课 | 把理解转成可运行 demo 或功能 | `lesson-types/implementation-lab.md.template` |
| 阶段复盘课 | 阶段验收、清理问题和复习计划 | `lesson-types/phase-review.md.template` |

---

## 🧪 理解检查 Rubric

评分标准见 `references/comprehension-rubric.md`。

| 等级 | 名称 | 推进判断 |
|---|---|---|
| 0 | Not Started | 不允许推进 |
| 1 | Exposure | 只算接触过，不允许推进 |
| 2 | Understanding | 默认最低通过线，允许推进 |
| 3 | Skill | 能迁移应用，允许推进 |
| 4 | Capability | 能设计/取舍/独立解决，允许推进 |

只有达到 Understanding 及以上，才允许把课程状态改为 `已完成`，并写入 `learning-records/` 和 `GLOSSARY.md`。

---

## 🧭 统一状态模型

`STATE.json`、`CURRENT.md`、`PROGRESS.md`、`COURSE-LIST.md` 和最新 handoff 统一使用以下状态：

```text
未开始 / 进行中 / 待理解检查 / 待补课 / 补课中 / 已完成 / 需复习 / 暂停
```

关键规则：

- `待理解检查`、`待补课`、`补课中` 不能直接进入下一节主线课。
- 只有状态为 `已完成`，才允许写入 `learning-records/` 和 `GLOSSARY.md`。
- 如果多个文件状态冲突，应先同步状态，再继续授课。

详细定义见 `references/status-model.md`。

---

## ✅ 工作区校验

```bash
python "${CLAUDE_SKILL_DIR}/scripts/validate_workspace.py" --root ./study
```

`validate_workspace.py` 只读不写，主要检查：

- 必需文件和目录是否存在。
- `STATE.json` 是否合法，`latest_handoff` 是否存在。
- 状态是否使用统一枚举。
- `PROGRESS.md` 与 `COURSE-LIST.md` 的同一课次状态是否一致。
- 未完成课程是否误填了 `learning-record`。
- handoff 文件名是否符合 `YYYY-MM-DD-Lxx-slug.md` 规范。
- 工作区内置模板是否齐全。

---

## 📚 示例与教程

- `docs/quickstart.md`：从安装到初始化、上第一课、校验工作区的完整流程。
- `examples/codebase-study-demo/`：源码项目学习示例，展示一套已经推进到 L01 完成状态的 `study/` 工作区。

---

## 🗺️ 后续计划

见 [`ROADMAP.md`](ROADMAP.md)。

---

## 📈 贡献与定制

- **扩充诊断问题**：修改 `references/diagnostic-questions.md` 添加全新的专业细分领域。
- **增加课程模板**：在 `templates/lesson-types/` 下定义更适合特定语言、考试或行业场景的专有课型模板。
- **扩展状态校验**：基于 `scripts/validate_workspace.py` 增加更严格的 `STATE.json` / Markdown 一致性检查。

---

## 📄 License

本项目采用 [MIT License](LICENSE) 许可协议。
