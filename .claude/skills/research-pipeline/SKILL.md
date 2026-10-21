---
name: research-pipeline
description: 一篇论文从确定方向到投稿的总入口（R0 方向 → R1 主线与故事 → R2 试点与实验协议 → R3 实验执行与故事结算 → R4 写作 → R5 评审与投稿）。用于开始一篇新论文、问"现在到哪一步 / 下一步做什么"、恢复中断的研究、要求按统一流程推进、判断能否进入下一阶段或需要回退、以及实验已经做完才来写论文（事后入口）时；负责判定当前阶段、核对门槛、把工作路由到对应阶段的 skill、维护 research/STATE.md 与 PROGRESS.md 并与 Codex 交接。自带项目骨架脚本与文件级门槛核对脚本。不替代各阶段 skill 本身，不运行实验，不写正文。 英文触发短语：where is this paper, what stage are we at, next step for the paper, start a new paper, resume the research, can we move to the next stage, roll back a stage, experiments are done how do we enter the pipeline, research pipeline, stage gates.
---

# Research pipeline：从方向到投稿

一篇论文是一个有先后顺序的流程：每个阶段有产出和门槛，门槛过了才进下一阶段；每个阶段结束都停下来等用户判断。本 skill 只做三件事：**判定阶段、核对门槛、路由与记录**。各阶段的内容由对应 skill 产出，本 skill 不代替它们。

Claude 与 Codex 共用同一份 `research/STATE.md` 和 `PROGRESS.md`，读同一套 skill。

## 阶段总览

| 阶段 | 目标 | 主要产出 | 门槛（用户确认后才过） | 路由到 |
|---|---|---|---|---|
| R0 方向 | 选出 2–3 个值得做、条件允许的方向并排序 | `docs/innovation-log.md`（每个方向一张四问潜力卡） | 用户选定排序，写下前提条件与已排除方向 | `innovation-explore` |
| R1 主线与故事 | 实验之前选定研究类型，定下主张、读者、RQ、判定规则、最强基线、潜力卡与 venue 候选，并写出带分支的故事骨架 | `paper/FRAMING.md`、`paper/STORY_SPINE.md`、`paper/VENUE_PROFILE.md` | 研究类型已声明（methods/ 档案名）；一句话主张；每个 RQ 有判定规则与阴性可解释的前提；基线是当前最强版本；骨架至少两个分支，各过删除测试、各有去处；潜力卡有前瞻档位；建议过一次 L1 | `paper-framing` → `paper-storytelling`（→ `paper-review` 的 L1） |
| R2 试点与实验协议 | 先小规模试做判分支和阈值，再按研究类型档案冻结确认协议 | `experiments/PILOT_<date>.md`（可免）、`experiments/PROTOCOL_<date>.md` + 指纹表 | 研究类型与 FRAMING 一致；试做已做并写回潜力卡与骨架，或写明免做理由；判定规则含三种结局与稳健性要求；结果中性检查已写；协议覆盖 venue 候选的 essential 属性并集；检查单全部勾选；用户确认冻结 | [pilot-protocol.md](references/pilot-protocol.md)、[experiment-protocol.md](references/experiment-protocol.md)、[methods/](references/methods/README.md) |
| R3 实验执行与结算 | 按协议做，结果进台账，按台账选定故事分支与 venue | `reports/<run>/RESULT.md`、`paper/ledger/*`、骨架结算节、归档的 R1 骨架、VENUE_PROFILE 的决定 | 每个 RQ 有判定且稳健性要求满足；偏离与事后分析已登记；台账齐全且关键结论有复核者；选定分支、归档 R1 版本、写下 venue 决定 | [experiment-run.md](references/experiment-run.md)、[when-results-disappoint.md](references/when-results-disappoint.md) + 项目自己的执行方式 |
| R4 写作 | 先图后文，按选定分支写 | `paper/FIGURE_PLAN.md`、`.paper-style/`、`paper/manuscript/`、`paper/state.json` | orchestrator 到 S5；S2 追加图表计划 + 风格合同 + 结算核对；编译干净；症状清单全否；每个数字可追到台账 | `paper-style-profiler` → `publication-chart-skill` / `scientific-visualization` → `paper-writing-orchestrator`（内部调用 `paper-storytelling`、`academic-humanizer`） |
| R5 评审与投稿 | 分级评审、修订、artifact、投稿材料 | `paper/review/`、artifact、S6–S7 | L3 结论为 GO_INTERNAL_REVIEW 或 GO_AFTER_TARGETED_REVISIONS 且修订已做；artifact 可验证；作者字段齐全 | `paper-review`（按 VENUE_PROFILE 加载 venue 档案）、`academic-humanizer`、orchestrator S6–S7 |

门槛细则见 [stage-gates.md](references/stage-gates.md)；R 阶段与 orchestrator S0–S7 怎样衔接、什么时候回退，见 [orchestrator-mapping.md](references/orchestrator-mapping.md)；venue 怎样影响协议而不影响结论，见 [venue-and-evidence-standards.md](references/venue-and-evidence-standards.md)。辅助 skill：`paper-reading` 在任何阶段做文献精读（R0 期间只用 `innovation-explore` 规定的压缩格式）。

## 使用方式

1. **判定阶段**：读 `research/STATE.md`、`PROGRESS.md` 和各阶段产出文件。阶段由产出和门槛决定，不由聊天措辞、提交数或谁最后说了什么决定。新项目没有 STATE.md 时先建骨架（已有的文件一律跳过，老项目也能跑）：

   ```bash
   python3 <skill_dir>/scripts/init_paper_project.py <项目目录> --paper-id <ID> --venue <venue 或 UNDECIDED>
   ```

   **实验已经做完才来写论文的项目**，按 [results-first-entry.md](references/results-first-entry.md) 的五步进入：冻结现状、事后 R1、决定要不要确认运行、从现有输出生成台账、正常进入 R4。时点如实标注，选择史写进 FRAMING。

   **已有自己文件布局的老项目**（R1–R4 的产物存在但名字不同）：不改名、不搬文件、不建空模板。`init_paper_project.py <项目目录> --state-only` 只建 STATE.md 与 PROGRESS.md，在 STATE.md 的阶段产出索引里写 `默认路径 → 实际路径`（如 `FRAMING → paper/latex/FRAMING-ARG.md`），`check_gates.py` 按索引找；"当前阶段"按产物实际到达的阶段填，"阶段历史"写明回填时点。写法见 [state-template.md](references/state-template.md)。
2. **核对门槛**：先跑文件级核对，再逐条对照 stage-gates 做人工判断：

   ```bash
   python3 <skill_dir>/scripts/check_gates.py <项目目录>        # 加 --json 给脚本读；--stage R2 指定阶段
   ```

   脚本只回答"文件在不在、格式对不对、哈希一不一致、状态值合不合同"；文件存在不等于门槛已过。退出码 0 是文件级全部通过，1 是有未过项，2 是读不到 STATE.md 且没给 `--stage`、`当前阶段` 行解析不出 R<n>，或 `--stage` 不在 R0–R5；非零不是脚本出错。任何一条不满足就报告"R<n> 门槛未过：<条目>"，不往下走。脚本报"缺失"而文件其实在别处时，先把路径登记进索引再跑，不要把"缺失"当成要回退。
3. **路由**：告诉用户当前应调用哪个 skill、做哪一件事、为什么，然后停下。用户说"继续 / 进入 R<n>"才进入该阶段的 skill。R0 的 `innovation-explore` 设了 disable-model-invocation，模型不能代为调用，只能请用户自己输入 `/innovation-explore`。
4. **记录**：阶段切换、阻塞、授权变化、会话结束时更新 `research/STATE.md`（核对时间、阶段、证据位置、剩余条件、下一步、待用户决定项、阶段历史）与 `PROGRESS.md`（任务行、交接记录）。规则见 [state-template.md](references/state-template.md)。
5. **回退**：后一阶段发现前一阶段的问题（写作时发现主张站不住、运行与协议不一致、评审给出 FATAL_CLAIM_GAP），明确写"回退到 R<n>，原因"，回到那个阶段的 skill 重做，不在当前阶段里打补丁。规则见 orchestrator-mapping.md 的"回退规则"。

## 流程里固定的规则

来自以往论文的教训，任何阶段都不得跳过：

- **先主线再实验。** R2 之前必须有 R1 的主张和主要比较；事后补的主线在 FRAMING 里记一行产生时点备查；正文按普通论文的做法写，不逐条标时点、不整篇降级（见 results-first-entry.md）。
- **每种结局都要有去处。** 骨架在实验之前就写成立与不成立两个分支，各有读者会改变的判断和退路 venue；结果中性检查让阴性结果可解释，是发现而不是失败。
- **基线必须是当前最强版本。** 与旧版本的对照不能写成对当前方法的优势。
- **判定规则必须带稳健性要求。** 重复运行用一致性规则（全部同号且均值过线），抽样用区间，定性用饱和与信度，理论用假设的最小集合；单次观察只能叫"单次观察"。研究类型不同，要求不同，写在 [methods/](references/methods/README.md) 的档案里。
- **venue 只改读者与收获。** 不改研究问题、主要比较、判定规则和主张强度；venue 对实验的影响只通过证据标准进入协议。
- **台账在 R3 生成，R4 只继承。** 正文数字从台账或输出文件引用，不手工抄；每个数字可追到 `reports/*/outputs`。
- **补做的分析内部分开记录**，不升格为协议内结论；正文里叫"分析"，不说成"验证"，不需要 post hoc 标签。
- **图表优先。** R4 开始前先定图一和图表清单，再定风格锚点，再写正文。
- **故事不改证据。** 骨架只决定顺序和重心；主张强度由台账决定；结算只选分支，不揉分支。
- **渐进式披露。** 每轮只推进一层，停下等用户；不一次给"完整方案"。
- **授权只来自用户的具体决定。** 训练、API、真实数据、保护集、投稿、外发各自独立，阶段状态不能推导授权。
- **评审一篇稿件要看渲染后的 PDF。** 版面、图表、字号一起看，不只读源码。

## 与 Codex 的交接

- 任务登记在 `PROGRESS.md` 的任务表：任务 ID、阶段、执行者、复核者、范围、完成条件、授权出处、状态。
- 一项工作一个执行者；同一文件被占用时先交接或用独立分支。
- 关键科学结论和大范围改动登记复核者，复核者实际查证据。
- 会话结束：更新 `research/STATE.md` 的"最近核对"与"下一步"，在 `PROGRESS.md` 写交接记录，写明未核实项。

## 交付

每次调用结束时用固定格式回答：

```
阶段：R<n> <名称>（上次核对 <日期>）
已过门槛：…
未过门槛 / 阻塞：…
待用户决定：…
下一步：调用 <skill>，做 <一件事>
```
