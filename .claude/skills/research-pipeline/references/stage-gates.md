# 阶段门槛细则

每条门槛都要能指向一个文件或一次用户决定。"看起来差不多"不算过。先跑 `scripts/check_gates.py` 做文件级核对，再逐条做下面的人工判断；脚本说"存在"只是存在。实验已经做完的项目按 [results-first-entry.md](results-first-entry.md) 进入，门槛相同，时点写事后。

## R0 方向 → R1

- `docs/innovation-log.md` 记录了候选思路、来源文献与用户筛选结果；"最终选定"有 2–3 个排序的方向，每个带四问潜力卡（重要在哪、谁在乎；合理的进攻路线；最脆弱假设与最小判别证据；答案反过来是否仍有人在乎）。
- 用户明确选定排序，并写下前提条件（数据形态、可用信号、算力、不做什么）。
- 已排除的方向有一句理由。
- 从观察起步的方向：innovation-log 的"异常入口"节有观察句与原始文件位置、伪像排查表（每行有结果，没有"未查"）、现象卡与文献对照；未排除的伪像写进前提条件，排查与刻画的产出标 exploratory。

## R1 主线与故事 → R2

- `paper/FRAMING.md`（模板：`paper-framing/references/framing-template.md`）：一句话主张；目标读者；RQ 列表，每个 RQ 有主要比较、指标、判定规则（怎样算成立、不成立、不能判定，稳健性要求按研究类型）和阴性结果可解释的前提；最强基线及其版本来源；明确不主张什么；潜力卡有前瞻档位；产生时点（事前 / 事后）。
- `paper/STORY_SPINE.md`：读者、原信念、张力有依据；至少两个分支（成立 / 不成立），每个分支的一句话故事 ≤40 字、删除测试为"是"、有适合的 venue 候选。
- `paper/VENUE_PROFILE.md`：2–3 个候选，每个有读者、贡献类型、essential 与 desirable 属性摘要、版式与流程、核验日期；写明协议必须覆盖的属性并集。
- 建议：`paper-review` 的 L1 前瞻用法：framing A/B 潜力门至少一个通过，两个分支都有去处；两个 framing 都不通过就不进入 R2，先重构问题。
- 用户确认主张、骨架与 venue 候选。

## R2 试点与实验协议 → R3

- 研究类型已声明（`- 研究类型：<档案名>`），对应的 [methods/](methods/README.md) 档案存在，档案要求的追加字段已填。
- 试做：`experiments/PILOT_<date>.md` 已完成并把结论写回潜力卡与骨架分支；或确认协议里写明"试点：免做，理由"。
- 确认协议：见 [experiment-protocol.md](experiment-protocol.md) 检查单，通用项与档案追加项全部勾选；判定规则写了成立、不成立、不能判定三种结局；稳健性要求按档案写明；结果中性检查已写；协议覆盖 venue 候选 essential 属性的并集；协议已冻结，指纹表在协议内（`scripts/hash_files.py` 生成的 `| 路径 | SHA-256 |` 表，`check_gates.py` 逐行复核）。

## R3 实验执行与结算 → R4

- 每个 RQ 有按协议规则得出的判定（成立 / 不成立 / 不能判定），稳健性要求按档案核对（重复一致、区间、饱和与信度、假设集合）；结果中性检查的结果已记录。
- `reports/<run>/RESULT.md` 记录：协议与指纹核对、完成情况（档案给的形式）、偏离登记、事后分析、输出文件清单。
- `paper/ledger/evidence_inventory.*` 与 `claim_ledger.*` 已生成，状态值使用 orchestrator 的合同（`VERIFIED_CURRENT` 等）。
- 事后分析单独登记，带"post hoc"与触发原因；结果不如预期的处置按 [when-results-disappoint.md](when-results-disappoint.md) 归类。
- 故事结算：R1 骨架已归档为 `paper/STORY_SPINE_R1_<date>.md`；`paper/STORY_SPINE.md` 的"结算"节选定了一个分支并给出证据 ID；`paper/VENUE_PROFILE.md` 的"决定"已填写理由。
- 关键结论在 `PROGRESS.md` 登记了复核者，复核者实际重算过。
- 原始数据、模型、日志按项目规则留在远端；本地只有轻量汇总。

## R4 写作 → R5

- orchestrator `paper/state.json` 到 `S5_VENUE_REVIEWED`。
- S2 追加项：`paper/FIGURE_PLAN.md`（每图一句结论，图一已定）、风格合同（`.paper-style/WRITING-CONTRACT.md`，validator 通过）、结算核对（选定分支依赖的证据仍是 `VERIFIED_CURRENT`，章节顺序与该分支一致）。
- 本地编译无未定义引用、无 overfull；`paper-storytelling` 第 4 节症状清单全部为否。
- 每个正文数字可追到台账或输出文件；正文不要求逐条标事前 / 事后，也不要求交代正文没出现的早期版本用过同一测试集。

## R5 评审与投稿 → 完成

- 分级评审（L1 → L2 → L3）最新结论为 GO 或 GO_AFTER_TARGETED_REVISIONS，修订已做并重新过 S4。
- L3 看过渲染后的 PDF：版面、图表、字号，不只读源码。
- 评审里 FAIL 而用户决定接受不回退的门（如 L2-G1 没有独立真值）：决定写进 `research/STATE.md` 的有效授权（日期、范围），补救措施（如补一份独立真值）或退路（收窄主张、换分支）及其期限写进阻塞 / 待用户决定；补救完成后该门重判。正文里的限制写在约束主张的位置，不只放附录。
- artifact 可验证（S6），作者字段、声明、DOI、投稿材料齐全（S7）。
- 投稿动作本身由用户执行。

## 回退

任何阶段发现更早阶段的问题，在 `research/STATE.md` 写"回退到 R<n>，原因"，回到那个阶段的 skill 重做，保留原阶段记录。换 venue 只重开 orchestrator 的 S2 并重写读者与收获，不动比较、规则和主张强度。常见触发见 [orchestrator-mapping.md](orchestrator-mapping.md) 的"回退规则"。
