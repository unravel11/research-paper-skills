# research/STATE.md 与 PROGRESS.md

两个文件都放在研究项目的仓库里，Claude 与 Codex 读写同一份。`research/STATE.md` 回答"现在在哪个阶段、门槛过了没、下一步做什么"；`PROGRESS.md` 回答"谁在做哪件事、做到哪、谁复核"。科学证据仍以各阶段产出文件为权威，这两个文件只做索引、门槛核对与交接。

模板在 [`assets/project-skeleton/`](../assets/project-skeleton/) 下；`scripts/init_paper_project.py` 把它们复制到新项目并填好论文 ID、venue 与日期，已有的文件一律跳过，所以老项目也可以直接跑。

## research/STATE.md

字段固定：论文 ID；目标 venue（可改，写原因）；当前阶段；最近核对（日期与执行者）；本地 / 远端 HEAD 与工作区状态；阶段产出索引；当前阶段门槛核对；有效授权；阻塞 / 待用户决定；下一步；未核实；阶段历史。

规则：

- 阶段切换、阻塞、授权变化、会话结束都更新"最近核对"和"下一步"，并在"阶段历史"加一行。
- 回退写明"回退到 R<n>，原因"，保留原阶段记录。
- 不在本文件里写结果数字；数字只引用台账或 RESULT.md。
- "有效授权"逐条引用用户的具体决定（日期、原话摘要、覆盖范围）。训练、API、真实数据、保护集、投稿、外发各自独立，阶段状态不能推导授权。
- `scripts/check_gates.py` 读"当前阶段"这一行，所以保持 `- 当前阶段：R<n> <名称>` 的格式。
- 评审里 FAIL 而用户决定接受不回退的门（如 L2-G1 没有独立真值）：决定写进"有效授权"（日期、范围），补救措施或退路及其期限写进"阻塞 / 待用户决定"；补救完成后该门重判。口头接受不算。

### 阶段产出索引：文件不在默认位置时

索引默认列出骨架的路径（`paper/FRAMING.md`、`experiments/PROTOCOL_<date>.md` 等）。项目把某个产物放在别处时，在对应阶段行里写 `默认路径 → 实际路径`，`check_gates.py` 先按索引找，没登记的按默认路径找：

```markdown
- R1：paper/FRAMING.md → paper/latex/FRAMING-ARG.md、STORY_SPINE → paper/latex/SKELETON.md
- R3：RESULT → paper/latex/stages/、paper/ledger/ → paper/latex/ledger/
- R4：FIGURE_PLAN → paper/latex/、.paper-style/ → paper/style/、manuscript → paper/latex/
```

写法：

- 箭头用 `→`、`->` 或 `=>` 都行；多项用 `、` 分开，也可以一项一行。路径后面的括号注释（如 `（事后）`）不算路径的一部分；HTML 注释整段忽略。
- 左边写默认路径或短名：`innovation-log`、`FRAMING`、`STORY_SPINE`、`VENUE_PROFILE`、`PILOT`、`PROTOCOL`、`RESULT`、`STORY_SPINE_R1`、`evidence_inventory`、`claim_ledger`、`FIGURE_PLAN`、`WRITING-CONTRACT`、`STYLE-STATE`、`manuscript`、`state.json`、`review`；`paper/ledger/` 与 `.paper-style/` 可以整个目录一起映射。不认识的名字脚本会提示并忽略。
- 右边是相对项目根的路径。单个文件的产物给目录时，按默认文件名在目录里找；`PROTOCOL`、`RESULT`、台账这类按模式匹配的产物给目录时，在目录及其子目录里按默认模式找；也可以直接给一个文件。
- 内容要求不随路径变：映射过去的台账仍要有 `status` 列并用合同里的状态值，骨架仍要有"## 分支"与"## 结算"。索引只告诉脚本去哪里找，不放松门槛。

### 已有自己文件布局的老项目

R1–R4 的产物已经存在、只是名字不同的项目，不为对齐模板改名、搬文件或建一套空模板：

1. `python3 scripts/init_paper_project.py <项目目录> --state-only` 只建 `research/STATE.md` 与 `PROGRESS.md`。
2. 把现有文件按上面的写法登记进阶段产出索引；"当前阶段"按产物实际到达的阶段填，不按模板的 R0。
3. "阶段历史"写一行："R1–R4 在接入流程前完成，<日期> 按产物回填，时点为事后登记"。事后的决定（主要比较、分支选择）在 FRAMING 与骨架里标"事后"。
4. 跑 `check_gates.py`；要回头核对早期阶段的产物用 `--stage R1` 等。

剩下的门槛逐条过，与新项目相同。

## PROGRESS.md

任务表每行一个任务：任务 ID、阶段、执行者（Claude / Codex / 用户）、复核者、范围、完成条件、授权出处、状态、备注。状态取值：待开始 / 进行中 / 待复核 / 完成 / 取消。

规则：

- 一项工作一个执行者；同一文件被占用时先交接或用独立分支。
- 关键科学结论和大范围改动必须有复核者；复核者实际查证据（读回执、重算、与独立实现对比），不是看一眼。完成前状态是"待复核"。
- 任务结束把交接写进"交接记录"：做了什么、证据在哪、未核实项、下一位该从哪开始。
- 不把聊天里的口头结论当完成；完成条件要能指向文件。
