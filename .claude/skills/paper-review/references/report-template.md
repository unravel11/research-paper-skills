# 分级评审报告模板

对话评审和落盘评审都用这个结构；栏目不删，没有信息写 `未验证`。证据指针紧跟结论。

## 结论先行

- 目标 venue：`<缩写与全称>`；档案：`references/venues/<venue>.md` 或 `通用量表（venue 未建档）`
- 评审层级：`L1 / L2 / L1+L2 / L3`
- 一句话结论：
- 潜力档位：`P3_STRONG / P2_VIABLE_CONDITIONAL / P1_WEAK_OR_UNFOCUSED / P0_NO_GO_CURRENT_DIRECTION / PU_ABSTAIN`，并标 `前瞻` 或 `已有证据`
- 补实验决定：`NO_MORE_CORE_EXPERIMENTS / ANALYSIS_ONLY / TARGETED_EXPERIMENTS / MAJOR_REDESIGN / ABSTAIN_MISSING_INPUTS`
- 当前允许执行的下一项工作：
- 不能声称的内容：
- 下一停止点：

## 1. 评审快照

| 项目 | 当前值 | 核验状态 |
|---|---|---|
| 日期 | | |
| 论文基线 / 路径 | | |
| 仓库、分支、完整 HEAD | | |
| 工作树 / 推送状态 | | |
| 实验版本 / 证据包 | | |
| 与上次评审的关系 | | |
| 当前官方规则 | `VERIFIED_CURRENT / ABSTAIN_NOT_VERIFIED / NOT_REQUESTED` | |

## 2. 当前 framing 与 claim ceiling

- 当前 framing：
- 允许的核心主张：
- 明确禁止的升级主张：
- 最关键的 load-bearing claim：

## 3. Framing A/B 潜力门

| 维度 | Framing A：当前定位 | Framing B：保守替代定位 |
|---|---|---|
| 一句话定义 | | |
| 直接证据 | | |
| 对目标 venue 读者的价值 | | |
| 最大缺口 | | |
| 所需新增工作 | | |
| 潜力档位 | | |

判定：`A / B / NO_CREDIBLE_FRAMING / ABSTAIN`，并写保留、削弱、删除的主张。

## 4. 主张与证据矩阵

| 论文主张 | 当前证据与路径 | 证据类别 | 支撑状态 | 可用表述 | 缺口 |
|---|---|---|---|---|---|
| | | | `PASS / PARTIAL / FAIL / ABSTAIN` | | |

分开写已验证事实、评审推断、未知。

## 5. Gate 结果

列出本层级全部核心门和 venue 附加门，不给总分。

| Gate | 状态 | 直接证据 | 对论文的影响 | 最小补救或停止条件 |
|---|---|---|---|---|

## 6. 主要科学问题

按对中心主张的影响递减排列；每条含受影响的主张、证据、后果。

## 7. venue 适配

- 读者价值：
- 领域专有要求（按档案）：
- 最近工作差异：
- 适配判断：`强 / 有条件 / 弱 / ABSTAIN`；不转换为接收预测。

## 8. 补实验与证据链决策

说明主决策如何由门结果推出。`TARGETED_EXPERIMENTS` 时逐张填量表里的实验卡片并按必要性排序；其他决定说明为什么新增运行解决不了当前问题。不执行实验。

## 9. 结果处置（L2 必填）

| 结果 / 表格 / 分析 | 处置 | 理由 |
|---|---|---|
| | `保留正文 / 降级表述 / 移入附录 / 历史保留 / 禁止使用 / 未解决` | |

## 10. artifact、伦理与披露

可复现性、机器可读证据、发布状态、匿名、人工审查、敏感细节、披露状态、授权，分别作为事实报告。

## 11. L3 专用：模拟审稿意见

- 渲染后 PDF 的版面与图表检查结果：
- Major comments：
- Minor comments：
- 前三条 load-bearing 拒稿风险：
- 推荐：`GO_INTERNAL_REVIEW / GO_AFTER_TARGETED_REVISIONS / NO_GO_MAJOR_REVISION / NO_GO_EVIDENCE_GAP / ABSTAIN_INCOMPLETE_MANUSCRIPT`
- 当前规则门：`VERIFIED_CURRENT / ABSTAIN_NOT_VERIFIED`，附核验日期与官方 URL

L1、L2 省略本节。

## 12. 已验证、推断与未验证

### 已验证事实
-
### 评审推断
-
### 未验证或缺失材料
-

## 13. 需要作者回答的问题

只问答案能改变门、framing 选择、档位或下一步的问题。

## 14. 下一停止规则

最小的下一步、可观察的完成条件、以及迫使降级、重构或弃权的条件；写明完成后应重新调用的层级。

---

# 落盘 JSON 记录

评审作为正式阶段门时，报告旁存 `REVIEW-RECORD.json`。`gate_results` 只示意一项，validator 要求本层级全部必需门都在。

```json
{
  "schema": "paper_review_record_v1",
  "review_level": "L1",
  "review_date": "2026-10-10",
  "target": {
    "venue": "<缩写>",
    "name": "<venue 全称>",
    "profile": "references/venues/<缩写>.md",
    "official_source_prefixes": ["https://<官方站点前缀>/"],
    "research_type": "<research-pipeline methods/ 档案名；L2 必填，其他层级可省>"
  },
  "snapshot": {
    "repository_or_source": "paper/main.tex",
    "branch": "main",
    "head": "0123456789abcdef0123456789abcdef01234567",
    "worktree_status": "clean",
    "manuscript_hashes": {
      "paper/main.tex": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
    },
    "evidence_bundle": "paper/ledger/evidence_inventory.csv",
    "artifact_version": "v1"
  },
  "gate_results": [
    {
      "id": "L1-G0",
      "status": "PASS",
      "evidence": ["git HEAD and SHA-256 manifest"],
      "impact": "The review is bound to one snapshot."
    }
  ],
  "framing": {
    "a": "当前 framing",
    "b": "最强保守替代，或 NO_CREDIBLE_ALTERNATIVE",
    "selection": "B"
  },
  "potential_tier": "P2_VIABLE_CONDITIONAL",
  "tier_basis": "evidence",
  "experiment_decision": "TARGETED_EXPERIMENTS",
  "major_findings": ["带证据与主张影响的发现"],
  "author_questions": ["能改变某个门的问题"],
  "next_stop_rule": "冻结的实验解决命名的主张缺口后停止。",
  "official_requirements": {
    "status": "NOT_REQUESTED",
    "verified_at": null,
    "sources": []
  }
}
```

`tier_basis` 取 `prospective`（R1 前瞻）或 `evidence`。L3 另加 `recommendation`，并包含 `L3-G0` 到 `L3-G9`；L2 或 `L1+L2` 包含全部 L1 与 L2 门。`profile` 没有档案时写 `generic`，`official_source_prefixes` 填该 venue 的官方页面前缀；有 `VERIFIED_CURRENT` 或 `ABSTAIN_NOT_VERIFIED` 时 `sources` 必须以这些前缀开头。validator 只查结构与枚举，不查科学真伪。
