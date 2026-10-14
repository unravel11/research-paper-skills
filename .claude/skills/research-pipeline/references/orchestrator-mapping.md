# R 阶段与 orchestrator S 阶段的对照

`research-pipeline` 管一篇论文从方向到投稿的 R0–R5；`paper-writing-orchestrator` 管稿件本身的 S0–S7。两套阶段不是并列的替代品：R 在外层决定"现在该做什么"，S 在 R4 和 R5 内部决定"稿件做到哪一步"。本文件写清两者怎样衔接，目的有两个：写作阶段不把前面已经定下的东西重新推导一遍；前面阶段的问题不被写作阶段的补丁盖住。

## 对照表

| R 阶段 | 产出 | 对应 S 门 | 衔接方式 |
|---|---|---|---|
| R0 方向 | `docs/innovation-log.md` | 无 | S 阶段不关心方向；R0 只影响 FRAMING 的"前提条件" |
| R1 主线与故事 | `paper/FRAMING.md`、`paper/STORY_SPINE.md`（带分支）、`paper/VENUE_PROFILE.md` | S2 的输入 | S2 不重新发明主张；它核对 FRAMING、结算后的分支与台账是否一致，补齐图表计划、风格合同之后才算锁定 |
| R2 试点与实验协议 | `experiments/PILOT_<date>.md`（exploratory）、`experiments/PROTOCOL_<date>.md` | S1 的 protocol / population / comparison set 字段 | 协议里的判定规则就是 claim ledger 里"允许强度"的来源；试点数据只能以 `EXPLORATORY_OR_CANDIDATE` 进台账 |
| R3 实验执行与结算 | `reports/<run>/RESULT.md`、`paper/ledger/*`、骨架结算节、归档的 R1 骨架、VENUE_PROFILE 的决定 | S1 Evidence locked；S0 的 target venue | S1 直接继承 R3 的台账，不在写作阶段重做台账；状态值用 orchestrator 的合同（`VERIFIED_CURRENT` 等）。S0 的 venue 来自结算的决定 |
| R4 写作 | `paper/FIGURE_PLAN.md`、`.paper-style/`、`paper/manuscript/`、`paper/state.json` | S0 → S5 | S0 定稿件权威与 venue；S1 继承台账；S2 锁定（含三项追加）；S3 先图后文；S4 一致性检查加症状清单；S5 第一轮 venue 评审（至少 L1） |
| R5 评审与投稿 | `paper/review/`、artifact、投稿材料 | S5 迭代 → S6 → S7 | L2、L3 评审与修订在 S5 循环；S6 artifact 验证；S7 投稿就绪。投稿动作由用户执行 |

## S2 的三项追加

R4 进入 S2 时，除 orchestrator 自己要求的（一句话主张、RQ、贡献对证据、大纲、图表计划、相关工作定位、不主张什么）之外，还必须有：

1. **图表计划**：`paper/FIGURE_PLAN.md` 每图每表一行，含"一句结论"（将成为图题第一句）、回答的 RQ 或骨架环节、数据来源（台账 ID 或输出文件）、不确定性规则、工具路线。图一先定，读者只看图一和图题就能复述转折。
2. **风格合同**：`paper-style-profiler` 从文献库里 3–5 篇优秀论文提炼的 `.paper-style/WRITING-CONTRACT.md`，其 validator 已通过。
3. **结算核对**：`paper/STORY_SPINE.md` 结算节选定的分支与台账一致：转折所依赖的证据 ID 状态仍是 `VERIFIED_CURRENT`；主张强度没有超过台账允许的措辞；大纲的章节顺序与该分支一致；R1 版本已归档。分支选错，或两个分支都站不住，回退 R1，不在 S2 里改骨架硬圆。

## 回退规则

- 写作阶段发现主张站不住（证据状态下调、主要比较不成立），回退 R1 重新 framing，而不是在 S3 里把措辞改弱了事。措辞改弱只适用于台账本来就只允许那个强度的情况。
- 写作阶段发现协议与运行不一致，回退 R3 在 RESULT.md 补差异记录；需要改协议时在 R2 追加补充协议，不改原文。
- 评审（S5）给出 `FATAL_CLAIM_GAP` 或 `MAJOR_REDESIGN`，回退到最早受影响的 R 阶段，由用户决定收窄主张还是补实验。
- 换 venue 不是回退：只重开 orchestrator 的 S2，重写读者、收获和相关工作邻域；研究问题、主要比较、判定规则、主张强度不动。规则见 [venue-and-evidence-standards.md](venue-and-evidence-standards.md)。
- 回退时在 `research/STATE.md` 写"回退到 R<n>，原因"，保留原阶段记录；orchestrator 的 `paper/state.json` 同步回到对应 S 门，不保留更晚的阶段标签。

## 评审层级在流程中的位置

| 时机 | 层级 | 目的 |
|---|---|---|
| R1 结束、R2 冻结前（建议） | L1 前瞻用法 | framing A/B 潜力门：这个主线值不值得投入正式实验；两个分支是否都有去处；结果中性检查是否已写 |
| R3 结束、进入 R4 前（可选） | L2 | 实验链审计：哪些结果可以进论文 |
| R4 的 S5 | L1（至少） | 第一轮 venue 评审 |
| R5 | L2 → L3 | 完整稿模拟审稿与 Go / No-Go；L3 必须看渲染后的 PDF |

评审统一用 `paper-review`，按 `paper/VENUE_PROFILE.md` 的 venue 加载档案（一个 venue 一个文件，按模板新建）；没有档案的 venue 用通用量表，安全 venue 另读 orchestrator 的 `security-venue-review.md`。评审只读；评审结论不授权改稿或跑实验。
