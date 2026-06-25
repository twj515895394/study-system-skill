---
name: study-system
description: "Use this skill whenever the user wants to systematically learn a complete body of material over time — a codebase/source repo, a course or textbook, an exam syllabus, an industry knowledge domain, a company SOP/process doc, a research paper set, or a child's school curriculum — and wants this to be a long-running, cross-session learning process rather than a single one-off explanation. Trigger on phrases like '系统学习', '帮我规划怎么学', '建一个学习计划/学习体系', '我要读懂这个项目/课程/资料', '陪我长期学X', '帮孩子补课/同步进度', '备考规划', or any request implying recurring study sessions on the same material across multiple conversations. Also trigger when the user has already started such a workspace (a `study/` folder with files like STATE.json, MASTER-PLAN.md, CURRENT.md, PROGRESS.md, handoffs/) and wants to continue, review progress, or start the next lesson. Do NOT trigger for a single quick question that doesn't need an ongoing plan."
---

# 通用学习体系 (Study System)

## 这个 Skill 解决什么问题

普通的“一节课讲解”模式有三个问题：没有主线（讲到哪算哪）、没有验收标准（讲完了≠学会了）、换个会话就断了（上下文全部重来）。

这个 Skill 把“教用户一个主题”变成“运营一个持续推进的学习工作区”：先搞清楚为什么学、学到什么程度、从哪开始，再把内容切成可消化的课，每课都验证理解、留下痕迹，下次会话能直接接上。

适用对象不限：源码项目、专业课、行业知识、企业 SOP、考试备考、孩子的学科辅导、论文阅读等都是同一套骨架，只是诊断问题和资料地图的命名会按领域换。

## 核心原则

1. **先建体系，再上课程。** 触发这个 skill 后，第一件事不是开讲，而是确认资料、目标、起点，并搭建学习工作区骨架。
2. **主线固定，补课动态。** 允许插入补基础课、概念复习、源码小课、设计练习等，但补课必须服务主线、不无限扩展，并在结束后回到主线。
3. **按掌握程度推进，不按天数推进。** 真正决定能否进入下一课的是理解检查是否通过。
4. **讲过 ≠ 学会了。** Exposure（讲过）、Understanding（理解）、Skill（能迁移）、Capability（能设计）是递进层级。只有用户真正展示出 Understanding 或更高，才允许把内容写进 `learning-records/` 或 `GLOSSARY.md`。
5. **状态必须一致。** `STATE.json`、`CURRENT.md`、`PROGRESS.md`、`COURSE-LIST.md`、最新 handoff 必须使用 `references/status-model.md` 中的统一状态，不要让多个文件互相矛盾。
6. **问题不等于补课。** 不阻塞当前主线的问题先进入 `QUESTION-PARKING-LOT.md`，不要让每个旁支问题都打断课程。
7. **通过不等于长期掌握。** 通过理解检查后，把关键知识点加入 `REVIEW-SCHEDULE.md`，后续用主动回忆和迁移题复习。
8. **先选课型，再写课程。** 单课前先判断是概念入门、源码调用链、架构拆解、论文阅读、练习复盘、动手实现还是阶段复盘，再选对应模板。
9. **能脚本化就脚本化。** 创建课程、生成 handoff、写 learning-record、课程收尾优先使用脚本，减少多文件手动同步导致的状态漂移。

## 标准工作流

### Step 1：确认资料与目标（轻量，必做）

简短确认资料类型、资料是否完整、最终希望产出什么。这一步不用问很多，1-2 句话即可，目的只是判断接下来怎么搭工作区。

### Step 2：轻量诊断（默认精简，可跳过）

默认从 `references/diagnostic-questions.md` 里挑该领域最相关的 **3-5 个**问题问用户，用来判断基础、目标偏应用还是理论、节奏偏好、是否需要补前置课。

如果用户明确表示想跳过，尊重这个意愿，直接进入 Step 3；但在生成的 `MISSION.md` 里注明“诊断已按用户要求跳过，以下目标基于用户自述”。

### Step 3：搭建学习工作区

运行初始化脚本，在用户当前项目或用户指定目录下创建 `study/` 骨架。安装为 Claude Code Skill 后，必须使用 `CLAUDE_SKILL_DIR` 引用脚本，不要假设当前目录就是 skill 仓库目录。

```bash
python "${CLAUDE_SKILL_DIR}/scripts/init_workspace.py" \
  --root ./study \
  --topic "<学习主题>" \
  --domain <领域>
```

初始化后会生成 `STATE.json`、核心 Markdown 看板、`QUESTION-PARKING-LOT.md`、`REVIEW-SCHEDULE.md`，并把课程/交接/学习记录/复习测验/多课型模板复制到 `study/_templates/`。

### Step 4：填充主计划

基于 Step 1/2 得到的信息，依次填写：

- `MISSION.md` —— 为什么学、成功图景、约束、暂不学什么
- `MASTER-PLAN.md` —— 唯一权威主计划：总目标、阶段路线、课程清单、阶段验收、动态补课规则、节奏
- `TEACHING-PROTOCOL.md` —— 教学风格协议
- `COURSE-ROADMAP.md` / `COURSE-LIST.md` —— MASTER-PLAN 的展开视图
- `STATE.json` —— 机器可读状态摘要，至少同步 topic、domain、current_status、reading_map
- 资料地图（文件名按 domain 而定）—— 按学习主线给资料排序，不是从头到尾机械列目录

### Step 5：单课循环

先根据课程目标选择课型，详见 `references/lesson-flow.md`。如果要创建课程文件，优先使用：

```bash
python "${CLAUDE_SKILL_DIR}/scripts/new_lesson.py" \
  --root ./study \
  --lesson-id <课次> \
  --title "<课程标题>" \
  --lesson-type <课型>
```

常用课型：`concept-primer`、`code-trace`、`architecture-walkthrough`、`paper-reading`、`exercise-review`、`implementation-lab`、`phase-review`、`generic`。

每节课只讲一个相对紧凑的主题。一课的最简骨架：目标 → 总览图 → 核心概念 → 资料/源码锚点 → 类比 → 小练习 → **理解检查** → 评分 → 视情况收尾或继续。

理解检查必须按 `references/comprehension-rubric.md` 评分，最低通过线默认是 Understanding。只达到 Exposure 不允许收尾。

如果出现有价值但不阻塞当前主线的问题，写入 `QUESTION-PARKING-LOT.md`，并说明后续处理策略；不要因为每个旁支问题都插补课。

### Step 6：课程收尾

通过理解检查后才执行收尾动作。优先用脚本减少状态漂移：

```bash
python "${CLAUDE_SKILL_DIR}/scripts/add_handoff.py" \
  --root ./study \
  --lesson-id <课次> \
  --title "<课程标题>" \
  --status 已完成

python "${CLAUDE_SKILL_DIR}/scripts/add_learning_record.py" \
  --root ./study \
  --topic "<已掌握知识点>" \
  --lesson-id <课次> \
  --mastery Understanding \
  --evidence "<通过证据>"

python "${CLAUDE_SKILL_DIR}/scripts/close_lesson.py" \
  --root ./study \
  --lesson-id <课次> \
  --title "<课程标题>" \
  --status 已完成
```

只有状态为 `已完成` 且掌握等级达到 Understanding 及以上时，才允许写入 `learning-records/`、`GLOSSARY.md`，并把关键知识点加入 `REVIEW-SCHEDULE.md`。

如果理解检查没通过，不要假装收尾。按 `references/dynamic-makeup-rules.md` 判断是否需要插入补课，补课结束后回到本课继续，而不是直接跳到下一课。

### Step 7：跨会话续接

新会话进入已有学习项目时，按 `references/handoff-protocol.md` 的顺序读取文件：README → STATE.json → MASTER-PLAN → MISSION → TEACHING-PROTOCOL → CURRENT → PROGRESS → 最新 handoff。不要每次都从头问用户“我们学到哪了”。

### Step 8：状态校验

在阶段收尾、新会话接手、或发现状态不一致时，运行：

```bash
python "${CLAUDE_SKILL_DIR}/scripts/validate_workspace.py" --root ./study
```

校验脚本只读不写。若出现 error，先修复状态和文件一致性，再继续授课。

## 理解检查 Rubric

评分标准见 `references/comprehension-rubric.md`。

| 等级 | 名称 | 推进判断 |
|---|---|---|
| 0 | Not Started | 不允许推进 |
| 1 | Exposure | 只算接触过，不允许推进 |
| 2 | Understanding | 默认最低通过线，允许推进 |
| 3 | Skill | 能迁移应用，允许推进 |
| 4 | Capability | 能设计/取舍/独立解决，允许推进 |

练习复盘、动手实现、架构借鉴等目标，最低通过线可以提高到 Skill 或 Capability。

## 统一状态模型

`STATE.json`、`CURRENT.md`、`PROGRESS.md`、`COURSE-LIST.md`、最新 handoff 必须统一使用以下状态：

未开始 / 进行中 / 待理解检查 / 待补课 / 补课中 / 已完成 / 需复习 / 暂停

详细规则见 `references/status-model.md`。

关键边界：

- 状态为 `待理解检查`、`待补课`、`补课中` 时，不允许直接进入下一节主线课。
- 只有状态为 `已完成`，才允许写入 `learning-records/` 和 `GLOSSARY.md`。
- 如果状态文件之间冲突，先同步状态，再继续授课。

## 动态补课判定

补课不是想插就插。判断要不要插入、插入哪种补课、补课后怎么回到主线，详见 `references/dynamic-makeup-rules.md`。

## 参考文件索引

| 文件 | 什么时候读 |
|---|---|
| `docs/script-commands.md` | 需要创建课程、生成 handoff、写 learning-record、课程收尾时 |
| `references/diagnostic-questions.md` | Step 2，按 domain 选诊断问题 |
| `references/lesson-flow.md` | Step 5，选择课型、设计单课结构、处理高概念密度内容 |
| `references/comprehension-rubric.md` | 理解检查评分、决定是否允许收尾/推进 |
| `references/dynamic-makeup-rules.md` | 发现理解断层、需要判断是否插补课时 |
| `references/handoff-protocol.md` | Step 7，新会话续接、写 handoff 时 |
| `references/status-model.md` | 任何涉及 STATE / CURRENT / PROGRESS / COURSE-LIST / handoff 状态更新时 |
| `templates/*.md.template` | 填充工作区各文件内容时的字段参考 |
| `templates/lesson-types/*.md.template` | 针对不同课型生成课程文档 |
| `scripts/init_workspace.py` | Step 3，一次性生成 study/ 骨架 |
| `scripts/new_lesson.py` | 创建新课并同步当前状态 |
| `scripts/add_handoff.py` | 创建 handoff 并同步 latest handoff |
| `scripts/add_learning_record.py` | 创建学习记录并同步复习计划 |
| `scripts/close_lesson.py` | 课程收尾，同步状态看板 |
| `scripts/validate_workspace.py` | Step 8，校验 study/ 工作区一致性 |

## 学习成果的检验标准

一个阶段/一门课结束，最终要能回答：学完后用户能做什么？能向别人解释什么？能设计什么？能解决什么实际问题？回到真实资料、源码、题目或业务场景时，用户是否能独立判断和迁移？
