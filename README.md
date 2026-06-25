# Study System - AI 伴学系统自定义 Skill

`study-system` 是一个专为 AI Agent（如 Claude, Gemini 等）设计的**持续伴学系统 Skill**。它将传统的“一问一答式教学”转变为“持续推进的学习工作区运营”，帮助用户在 AI 的协助下，系统化、有步骤、有反馈地吃透任何一个复杂的知识领域或项目。

---

## 🚀 解决的痛点

在传统的 AI 教学/伴学场景中，通常存在以下三个痛点：
1. **缺乏主线**：走到哪讲到哪，学习进度容易失控或跑偏。
2. **没有验收标准**：AI 讲完了不等于用户学会了。缺乏有效的主动理解检查。
3. **跨会话上下文丢失**：新开一个 Chat 窗口，之前学到哪里、掌握到什么程度全部丢失，需要重新对齐。

`study-system` 通过在用户项目根目录下构建一个**持久化、可追踪的学习工作区 (`study/` 目录)**，让 AI 能够像教练一样，跨会话地追踪用户的学习进度、进行理解检查，并动态插入补课计划。

---

## 🧠 核心设计原则

1. **先建体系，再上课程**：不盲目开讲。在正式开始学习前，必须先理清学习目标（Mission）、主计划（Master Plan）和起点，搭建结构化的骨架。
2. **主线固定，动态补课**：学习主线保持清晰，允许因基础薄弱随时插入“补课”或“概念复习”，但补课必须有明确的目的和边界，且结束后必须回到主线。
3. **按掌握程度推进，不按时间推进**：摒弃机械的“X天计划”，只有在用户通过“理解检查”后，才能进入下一课。
4. **“讲过”不等于“学会了”**：严格区分 **Exposure (接触过)** 和 **Understanding (理解了)**。只有用户能用自己的话解释或通过场景题测试，才能将知识记录在学习档案中。

---

## 📂 项目目录结构

本仓库是一个完整的 Custom Skill 资源包，目录结构如下：

```text
study-system/
├── SKILL.md                 # 核心 Skill 定义文件，包含 Agent 的触发规则、原则及工作流指令
├── README.md                # 本说明文件
├── scripts/
│   └── init_workspace.py    # 用于在用户项目中初始化 study/ 学习工作区的 Python 脚本
├── references/              # 指导 Agent 执行伴学动作的参考规范（Markdown 格式）
│   ├── diagnostic-questions.md # 5个核心领域的轻量诊断问题模板
│   ├── lesson-flow.md          # 单课教学流程设计及“理解检查”方法论
│   ├── dynamic-makeup-rules.md # 动态补课的触发判定与规则表
│   └── handoff-protocol.md     # 跨会话续接时的文件读取与交接规范
└── templates/               # 工作区各类文档的模板文件（供初始化脚本调用）
    ├── MASTER-PLAN.md.template # 唯一权威主计划模板
    ├── MISSION.md.template     # 学习使命与边界模板
    ├── CURRENT.md.template     # 当前学习状态模板（新会话优先读取）
    ├── PROGRESS.md.template    # 整体进度看板模板
    └── ...                     # 其他阶段路线图、术语表、交接单等模板
```

---

## 🛠️ 快速开始

### 1. 注册为 Agent 的 Custom Skill
你可以将此项目复制到 AI 客户端/Agent 的自定义技能配置目录下（例如 `.agents/skills/study-system/`）。
* **触发词**：系统学习、建一个学习计划、我要读懂这个项目/课程、帮我规划怎么学、陪我长期学等。

### 2. 初始化学习工作区
当触发 Skill 时，AI 会引导你进行轻量诊断，确认你的目标与资料情况，并在你的项目根目录下执行脚本来初始化工作区：

```bash
# 在当前项目初始化一个关于 "RAG系统" 的源码学习工作区
python scripts/init_workspace.py --root ./study --topic "RAG 系统原理" --domain code
```

#### 参数说明：
* `--root`: 工作区根目录，默认 `./study`。
* `--topic`: 学习主题名称。
* `--domain`: 学习领域，决定生成的资料地图文件名。
  * `code` -> `SOURCE-READING-MAP.md` (源码阅读地图)
  * `course` -> `TEXTBOOK-READING-MAP.md` (教材阅读地图)
  * `industry` -> `RESOURCE-READING-MAP.md` (资料阅读地图)
  * `exam` -> `EXAM-ROADMAP.md` (考试路线图)
  * `child` -> `SCHOOL-SYNC-PLAN.md` (学校同步进度图)
  * *亦可传入其他自定义字符串，如 `research`。*
* `--reading-map-name`: 自定义资料地图文件名（覆盖 domain 默认）。
* `--reading-map-title`: 自定义资料地图标题。
* `--diagnosis-mode`: 诊断模式说明。

---

## 🔄 标准工作流 (The 7-Step Workflow)

```mermaid
graph TD
    A[Step 1: 确认资料与目标] --> B[Step 2: 轻量诊断/确认基础]
    B --> C[Step 3: 运行脚本初始化 study/ 骨架]
    C --> D[Step 4: 填充 MISSION.md 与 MASTER-PLAN.md]
    D --> E[Step 5: 单课循环 - 讲解与理解检查]
    E -->|未通过| F[动态判定: 插入补课并回溯]
    F --> E
    E -->|通过| G[Step 6: 更新进度与 CURRENT.md, 写入 handoffs/]
    G --> H[Step 7: 跨会话续接 - 优先读取 CURRENT & handoff]
    H --> E
```

### 详细步骤说明：

1. **确认资料与目标 (Step 1)**：AI 明确用户的资料来源（代码、教材、论文等）以及期望达到的终点状态。
2. **轻量诊断 (Step 2)**：AI 从 `references/diagnostic-questions.md` 选取 3-5 个针对性问题，摸清用户基础，制定合适坡度。
3. **搭建工作区 (Step 3)**：AI 调用脚本，在项目目录下生成 `study/` 目录及 10+ 个核心看板 and 计划文件。
4. **填充主计划 (Step 4)**：AI 细化填充 `MASTER-PLAN.md`（课程清单与阶段验收标准）和 `MISSION.md`（定义阶段成功图景）。
5. **单课循环 (Step 5)**：
   * 采用“一课一主题”设计。
   * 课后进行严格的**理解检查 (Comprehension Check)**，杜绝“懂了吗”这种流于表面的提问，改用类比、写流程、做边界设计等方式检验。
6. **收尾与记录 (Step 6)**：
   * 只有通过检查，才能更新 `PROGRESS.md`，并在 `learning-records/` 下写学习日志。
   * 每次对话结束前，AI 会在 `handoffs/` 生成一个**交接单 (Handoff)**。
7. **跨会话续接 (Step 7)**：新对话开始时，AI 优先读取 `CURRENT.md` 和最新 `handoff` 快速热启动，直接对齐上节课的内容。

---

## 📈 贡献与定制

该系统模板可以根据你特定的教学理念或项目性质进行扩展：
* **扩充诊断问题**：修改 `references/diagnostic-questions.md` 添加全新的专业细分领域。
* **增加课程模板**：在 `templates/` 下定义更适合特定语言（如 Go/Rust）或特定类型考试的专有课表模板。

---

## 📄 License

本项目采用 [MIT License](LICENSE) 许可协议。
