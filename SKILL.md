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

这几条是判断力的来源，不是死板 checklist。遇到没有覆盖的情况，回到这些原则推理该怎么做。

1. **先建体系，再上课程。** 触发这个 skill 后，第一件事不是开讲，而是确认资料、目标、起点，并搭建学习工作区骨架。
2. **主线固定，补课动态。** 允许插入补基础课、概念复习、源码小课、设计练习等，但补课必须服务主线、不无限扩展，并在结束后回到主线。
3. **按掌握程度推进，不按天数推进。** “30天计划”之类的节奏只是参考，真正决定能否进入下一课的是理解检查是否通过。
4. **讲过 ≠ 学会了。** exposure（讲过）、understanding（答对）、skill（能迁移）、capability（能设计）是递进层级。只有用户真正展示出 understanding 或更高，才允许把内容写进 `learning-records/` 或 `GLOSSARY.md`。
5. **状态必须一致。** `STATE.json`、`CURRENT.md`、`PROGRESS.md`、`COURSE-LIST.md`、最新 handoff 必须使用 `references/status-model.md` 中的统一状态，不要让多个文件互相矛盾。
6. **问题不等于补课。** 不阻塞当前主线的问题先进入 `QUESTION-PARKING-LOT.md`，不要让每个旁支问题都打断课程。
7. **通过不等于长期掌握。** 通过理解检查后，把关键知识点加入 `REVIEW-SCHEDULE.md`，后续用主动回忆和迁移题复习。

## 标准工作流

### Step 1：确认资料与目标（轻量，必做）

简短确认资料类型（源码/教材/讲义/课程视频/论文/业务文档/SOP/题库/行业报告等）、资料是否完整、最终希望产出什么（笔记/项目/方案/考试成绩/能力证明等）。这一步不用问很多，1-2句话即可，目的只是判断接下来怎么搭工作区。

### Step 2：轻量诊断（默认精简，可跳过）

默认从 `references/diagnostic-questions.md` 里挑该领域最相关的 **3-5 个**问题问用户（不是机械问满8个），用来判断基础、目标偏应用还是理论、节奏偏好、是否需要补前置课。

先检查用户第一句话里有没有已经回答过的。如果用户已经说清楚了目标、产出、资料情况，不要把模板问题原样照搬再问一遍，只问还缺的信息。

如果用户明确表示想跳过（例如“直接开始”“不用问了”“我已经想清楚了”），尊重这个意愿，直接进入 Step 3；但在生成的 `MISSION.md` 里注明“诊断已按用户要求跳过，以下目标基于用户自述”。

### Step 3：搭建学习工作区

运行初始化脚本，在用户当前项目或用户指定目录下创建 `study/` 骨架。安装为 Claude Code Skill 后，必须使用 `CLAUDE_SKILL_DIR` 引用脚本，不要假设当前目录就是 skill 仓库目录。

```bash
python "${CLAUDE_SKILL_DIR}/scripts/init_workspace.py" \
  --root ./study \
  --topic "<学习主题>" \
  --domain <领域>
```

初始化后会生成 `STATE.json`、核心 Markdown 看板、`QUESTION-PARKING-LOT.md`、`REVIEW-SCHEDULE.md`，并把课程/交接/学习记录模板复制到 `study/_templates/`，方便跨 Agent 续接。

`--domain` 决定资料地图文件名。`code/course/industry/exam/child` 是5个常见预设（源码项目用 `SOURCE-READING-MAP.md`，专业课用 `TEXTBOOK-READING-MAP.md`，行业学习用 `RESOURCE-READING-MAP.md`，备考用 `EXAM-ROADMAP.md`，孩子课程用 `SCHOOL-SYNC-PLAN.md`），但不是穷举。传其他字符串（比如 `research`）也不会报错，会落到通用命名，也可以加 `--reading-map-name` / `--reading-map-title` 完全自定义。

脚本只生成骨架和占位内容，具体内容仍需要结合 Step 1/2 的信息填进去。

### Step 4：填充主计划

基于 Step 1/2 得到的信息，依次填写：

- `MISSION.md` —— 为什么学、成功图景、约束、暂不学什么
- `MASTER-PLAN.md` —— 唯一权威主计划：总目标、阶段路线、课程清单、阶段验收、动态补课规则、节奏
- `TEACHING-PROTOCOL.md` —— 教学风格协议（在第一节课结束前，必须与用户明确偏好并初始化，规定风格、概念极限、图表及理解检查偏好）
- `COURSE-ROADMAP.md` / `COURSE-LIST.md` —— MASTER-PLAN 的展开视图
- `STATE.json` —— 机器可读状态摘要，至少同步 topic、domain、current_status、reading_map
- 资料地图（文件名按 domain 而定）—— 按学习主线给资料排序，不是从头到尾机械列目录

如果用户的目标是“先系统学懂一个领域/项目，再落地一个具体产出”，把“学懂”和“能落地”拆成不同阶段，分开验收。

所有路线图、清单、进度表都要服务于 `MASTER-PLAN.md`，发现冲突时以它为准。

### Step 5：单课循环

每节课只讲一个相对紧凑的主题。节奏和高概念密度课程的特殊处理见 `references/lesson-flow.md`，模板见 `templates/lesson.md.template`，工作区内副本见 `study/_templates/lesson.md.template`。

一课的最简骨架：目标 → 总览图 → 核心概念 → 资料/源码锚点 → 类比 → 小练习 → **理解检查** → 视情况收尾或继续。

理解检查不能只问“懂了吗”，要让用户用自己的话解释、做对照表、画流程、判断边界、设计小方案、回答场景题等。只有理解检查通过才进入收尾。

如果出现有价值但不阻塞当前主线的问题，写入 `QUESTION-PARKING-LOT.md`，并说明后续处理策略；不要因为每个旁支问题都插补课。

### Step 6：课程收尾

通过理解检查后才执行收尾动作：更新 `STATE.json`、`PROGRESS.md`、`CURRENT.md`、写一份 `handoffs/`、更新对应的 `reference/`，必要时写 `learning-records/`、`GLOSSARY.md`、`NOTES.md`。若风格偏好改变，同步更新 `TEACHING-PROTOCOL.md`。

只有状态为 `已完成` 时，才允许写入 `learning-records/`、`GLOSSARY.md`，并把关键知识点加入 `REVIEW-SCHEDULE.md`。

如果理解检查没通过，不要假装收尾。按 `references/dynamic-makeup-rules.md` 判断是否需要插入补课，补课结束后回到本课继续，而不是直接跳到下一课。

### Step 7：跨会话续接

新会话进入已有学习项目时，按 `references/handoff-protocol.md` 的顺序读取文件：README → STATE.json → MASTER-PLAN → MISSION → TEACHING-PROTOCOL → CURRENT → PROGRESS → 最新 handoff。不要每次都从头问用户“我们学到哪了”。

### Step 8：状态校验

在阶段收尾、新会话接手、或发现状态不一致时，运行：

```bash
python "${CLAUDE_SKILL_DIR}/scripts/validate_workspace.py" --root ./study
```

校验脚本只读不写。若出现 error，先修复状态和文件一致性，再继续授课。

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
| `references/diagnostic-questions.md` | Step 2，按 domain 选诊断问题 |
| `references/lesson-flow.md` | Step 5，设计单课结构、处理高概念密度内容 |
| `references/dynamic-makeup-rules.md` | 发现理解断层、需要判断是否插补课时 |
| `references/handoff-protocol.md` | Step 7，新会话续接、写 handoff 时 |
| `references/status-model.md` | 任何涉及 STATE / CURRENT / PROGRESS / COURSE-LIST / handoff 状态更新时 |
| `templates/*.md.template` | 填充工作区各文件内容时的字段参考 |
| `scripts/init_workspace.py` | Step 3，一次性生成 study/ 骨架 |
| `scripts/validate_workspace.py` | Step 8，校验 study/ 工作区一致性 |

## 学习成果的检验标准

一个阶段/一门课结束，最终要能回答：学完后用户能做什么？能向别人解释什么？能设计什么？能解决什么实际问题？回到真实资料、源码、题目或业务场景时，用户是否能独立判断和迁移？
