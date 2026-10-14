---
name: paper-review
description: 分级评审任何目标 venue 的论文、实验结果或研究计划（L1 主线与潜力门 / L2 证据链审计 / L3 投稿前模拟审稿）。先从用户指定或 paper/VENUE_PROFILE.md 读出 venue，加载对应的 venue 档案（按模板为每个 venue 新建一份），没有档案就用通用量表加官方来源协议。用于用户要求一级/二级/三级评审、判断 framing（兼容口语 farming）是否被证据支撑、决定要不要补实验、做投稿 Go/No-Go、模拟审稿、或在 R1 实验之前做前瞻潜力评估时；未指定层级默认 L1。英文触发短语：review this paper for a given venue, graded review, L1 L2 L3 review, framing review, is the framing supported by the evidence, should we run more experiments, go or no-go, simulate the reviewers, pre-submission check, venue fit, potential tier. 只读：不改稿、不跑实验、不预测录用概率。不用于只查 venue 事实（分区、费用、周期）、不用于经济学期刊的审稿量表、不用于改写稿件。
---

# 分级评审：venue 无关的核心加 venue 档案

同一套评审骨架适用于所有 venue：快照、证据账本、framing A/B、主张与证据映射、逐门判定、补实验决策。venue 之间真正不同的只有读者是谁、奖励什么贡献、领域专有的附加门、L3 要核对的官方规则。这些差异写在 venue 档案里，核心量表不为任何一个期刊定制。

## 基本原则

- 用户说的 farming 按论文语境理解为 framing，不借机改研究本意。
- 默认只读。除非用户明确要求，不修改论文、实验、分支或评审记录。
- 把"实验完成""validator 通过""论文可编译""科学证据充分""具有投稿潜力"分开判断。
- 不把 source candidate、controlled transfer、development-only、retrospective、silver label、mechanical validation 或 exploratory evidence 升级为漏洞、人工 gold、SOTA、因果、普遍泛化或投稿就绪。
- 不因为项目是先做实验后写论文、或测试集被用过多次，就整篇降级或降档；只看方法是否在开发集上定、结论是否超过证据量。正文没出现的早期版本在同一测试集上评过，不要求披露。
- 缺少权威输入时用 `ABSTAIN` 并列出缺失材料，不自行补事实。
- 潜力档位是对 framing、证据链和稿件完整性的判断，不是接收概率。用户要概率时拒绝，用档位、就绪度和拒稿风险代替。

## 先定 venue，再选档案

1. venue 的来源按优先级：用户本次指定；`paper/VENUE_PROFILE.md` 的"决定"；它候选表的第一行；都没有就问用户，或按通用量表评审并在报告里标"venue 未定"。
2. 按缩写在 [references/venues/](references/venues/) 找档案。有档案（按模板新建，一个 venue 一个文件）就加载它的读者与贡献类型、附加门、L1 适配问题、L3 核对项和官方来源前缀。没有档案就用通用量表加 [official-source-protocol.md](references/official-source-protocol.md)，并提示可按 [venues/README.md](references/venues/README.md) 新建一份。安全会议另读 orchestrator 的 `security-venue-review.md`。
3. 不把一个 venue 的档案套到另一个 venue：软件工程期刊与安全应用期刊的读者和证据要求不同，缩写相近也不能混用。也不用面向经济学期刊的审稿量表。
4. 只查 venue 事实（分区、费用、审稿周期）不是评审，按官方来源协议直接查，标提供方、年份和核验日期。

## 选择评审层级

| 层级 | 默认用途 | 必须回答的问题 |
|---|---|---|
| 一级 L1 | 默认；高频进展评审；R1 实验之前的前瞻用法 | 现有证据，或前瞻时的潜力卡与骨架分支，是否支撑 framing？有没有更保守但更站得住的 framing？该停止、补分析、补实验还是重构？ |
| 二级 L2 | 协议冻结后、改稿前或发现污染时 | 从对象到结论的证据链站不站得住：对象与分母、真值与度量、隔离、分析单位、过程受控、对照、判定与不确定性、稳健性、复现链？按研究类型的问法审。哪些结果可以进论文？ |
| 三级 L3 | 完整稿形成后 | 以目标 venue 审稿人的视角评估新颖性、方法、实验、写作、可复现性、venue 契合度、版面与图表，给出 Go / No-Go。 |

可组合，如 `L1+L2`。未指定只做 L1。稿件不完整时 L3 降级为 L1 或 L2，或返回 `ABSTAIN_INCOMPLETE_MANUSCRIPT`，不假装做了 L3。

## 在 research-pipeline 中的位置

- R1 结束、R2 冻结前：L1 的前瞻用法。材料是 FRAMING 的潜力卡、带分支的 STORY_SPINE 和 VENUE_PROFILE，不是结果。判定规则与结果中性检查是否写定、基线是否当前最强、两个分支是否都有去处；档位标"前瞻"，试点或 R3 后重新给档。两个 framing 都不过就回 `paper-framing`，不进 R2。
- R3 结束、进入 R4 前（可选）：L2，决定哪些结果可以进论文。
- R4 的 S5：至少一次 L1。
- R5：L2 到 L3。L3 必须渲染 PDF 看版面与图表，不只读源码。
- 报告存 `paper/review/`；结论与补实验决策同步到 `research/STATE.md` 的"待用户决定"。

## 加载参考资料

- 每次评审完整读 [references/review-rubric.md](references/review-rubric.md)，再读选定的 venue 档案。
- 做 L2 时读 [references/l2-by-method.md](references/l2-by-method.md)：先从 `experiments/PROTOCOL_*.md` 第一行读研究类型（没有就看 FRAMING 或问用户），按对应小节的问法审十门；类型名以 `research-pipeline/references/methods/` 的档案名为准。
- 生成报告时读 [references/report-template.md](references/report-template.md)。
- L3，或任何涉及当前 scope、投稿规则、格式要求的判断，读 [references/official-source-protocol.md](references/official-source-protocol.md)，只用官方页面并标核验日期。

## 评审工作流

1. **冻结评审快照。** 记录日期、仓库或路径、分支、完整 HEAD、工作树状态、论文基线、实验版本、可见材料、被替代的上次评审。先读当前工作区的 `AGENTS.md` 或 `CLAUDE.md`；项目规定了远端权威仓库或连接 skill 就遵循它。不从分支名、目录名或历史报告推断权威。脏工作树可以评，但要标明并绑定文件哈希。材料不完整时继续做能做的部分，同时降低结论等级；没有正文时只能评"研究方案"，不能声称论文有投稿潜力。
2. **建立证据账本。** 每项材料标为 `VERIFIED_CURRENT` / `CONTROLLED_OR_RETROSPECTIVE` / `EXPLORATORY_OR_CANDIDATE` / `SUPERSEDED_OR_INVALID` / `MISSING_OR_UNRESOLVED`，与 research-pipeline 台账和 orchestrator 合同同名。每个主张记录证据路径、适用数据与指标、验证状态和 claim ceiling。类别之间不靠措辞升级。
3. **framing A/B 潜力门。** A 是当前采用的核心定位，B 是同一证据能支撑的最强保守替代，不凭空加贡献。比较研究问题清晰度、证据覆盖、venue 价值、可区分贡献、残余风险、需新增的工作。没有真实的 B 写 `NO_CREDIBLE_ALTERNATIVE`。至少一个 framing 过最低潜力门才建议投入新的正式实验；两个都不过，优先重构问题，不通过大规模实验找正结果。
4. **主张与证据映射。** 逐项检查问题、方法或干预、数据与比较、结果、结论。结果不能唯一支撑的表述降级或标缺口。必须区分：检索覆盖与候选内决策质量；相关性与因果；同池比较与端到端比较；development 或 retrospective 与 untouched confirmation；controlled implementation 与 faithful reproduction；标识符锚定的参照标签与人工语义 gold；局部结论与跨系统、跨时间泛化。
5. **逐门判定。** 核心门按量表，L2 的十门按研究类型的问法，venue 附加门按档案；每门只用 `PASS` / `PARTIAL` / `FAIL` / `ABSTAIN`，不给总分，不把 `ABSTAIN` 当 `PASS`。
6. **补实验决策。** 只选一个：`NO_MORE_CORE_EXPERIMENTS` / `ANALYSIS_ONLY` / `TARGETED_EXPERIMENTS` / `MAJOR_REDESIGN` / `ABSTAIN_MISSING_INPUTS`。每个建议的实验用量表里的实验卡片，写清它填补的主张缺口、最小设计、独立验证、各种结果下论文怎么变、停止规则、无论结果如何都不能声称什么。不写"多加数据、基线、消融"。
7. **L3 专项。** 渲染 PDF 看版面与图表：图一是否在前两页并能单独讲出转折，表格与字号是否可读，是否被压缩，`paper-storytelling` 的症状清单是否全否。按官方来源协议核验当前 scope 与投稿规则，访问失败只对管理字段 `ABSTAIN_NOT_VERIFIED`，不影响科学结论。列前三条拒稿风险并给一个允许的推荐。
8. **重复评审。** 有上次评审时先验证其快照是否仍适用，再报告新增证据、被替换结果、门禁变化、framing 变化和补实验决策变化。没有可比快照写 `NO_VERIFIED_PRIOR_SNAPSHOT`。

## 输出要求

- 用用户的语言，默认中文，稿件术语与引文保持原文。先给结论和补实验决策，再给证据。
- 用 report-template.md 的结构；没有信息的栏目保留 `未验证`，不删关键门禁。
- 所有结论给材料路径或来源位置；远端状态说明是否已推送。
- 明确区分已验证事实、评审推断、仍未验证。
- 不因用户希望投稿而提高档位，也不因单一负结果否定有证据支撑的保守 framing。

## 持久化记录

用户要求保存，或评审被用作正式阶段门时：按模板保存可读报告，并存同名 `REVIEW-RECORD.json`（schema `paper_review_record_v1`，结构见 report-template.md），然后运行

```bash
python3 <skill_dir>/scripts/validate_review_record.py paper/review/<name>/REVIEW-RECORD.json
```

validator 只查结构、枚举、必需门和官方来源前缀，不证明证据为真、论文就绪或会被接收。普通对话评审不落盘，除非用户要求。

## 完成标准

评审快照、证据账本、framing A/B、claim ceiling、潜力档位（含前瞻或已有证据的标注）、补实验主决策、下一停止点都明确，才算完成。
