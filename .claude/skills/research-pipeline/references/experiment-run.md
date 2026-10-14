# R3 执行：按协议做，结果进台账

执行本身用项目自己的运行方式（脚本、队列、访谈、证明助手）；本 reference 只规定执行的纪律和产出。研究类型特有的记录项见 [methods/](methods/README.md) 对应档案的"RESULT 追加小节"。

## 开始前

- 核对协议指纹：脚本、配置、量表、编码本与协议表一致；不一致就先登记偏离，不悄悄改。
- 核对环境与版本、授权（真实数据、API、参与者招募、外发各自独立）。
- 登记 `PROGRESS.md` 的任务行：执行者、复核者、完成条件。

## 执行中

- 协议只追加不修改：新情况写补充协议并记日期。
- 失败、重做、中断如实登记：原因、是否影响已完成部分、重做是否在同一协议下。
- 不中途看确认性结果来调整设计；需要看就记为偏离，并说明看到了什么。
- 原始数据、模型、录音、日志按项目规则留在远端或受控位置，本地只放轻量汇总。

## 结束后：RESULT.md

```markdown
# RESULT：<run 或批次名>
- 研究类型：

## 协议与指纹核对
- 协议文件与冻结时间；指纹逐项一致 / 不一致项与处理

## 完成情况
- 按档案给的形式：运行表、对象表、参与者流程（招募 → 排除 → 分析）、证明状态表

## 结果中性检查
- 每项检查的结果；不通过的 RQ 标"不能判定"

## 判定（每个 RQ 一条）
- 成立 / 不成立 / 不能判定；按协议规则得出；稳健性要求是否满足（重复一致、区间、饱和、假设集合）

## 偏离登记
- 日期、内容、理由、谁决定、对结论的影响；无偏离写"无"

## 事后分析（post hoc）
- 看过结果后新增的分析：触发原因、是否影响主张；内部记录，不升格为协议内结论

## 输出文件清单
- 每个要进正文的数字对应的输出文件

## 同步与未核实
- 远端位置、未核实项、下一位该从哪开始
```

## 台账

- 证据台账 `paper/ledger/evidence_inventory.*`：每条证据一行，状态用合同里的五个值（`VERIFIED_CURRENT` / `CONTROLLED_OR_RETROSPECTIVE` / `EXPLORATORY_OR_CANDIDATE` / `SUPERSEDED_OR_INVALID` / `MISSING_OR_UNRESOLVED`）。
- 主张台账 `paper/ledger/claim_ledger.*`：每个主张一行，状态用 `SUPPORTED` / `WEAKEN` / `ABSTAIN` / `REMOVE_FROM_CURRENT_CHAIN`，依据指向证据 ID。
- 正文数字只从台账或输出文件引用，不手工抄。

## 结果不如预期

按 [when-results-disappoint.md](when-results-disappoint.md) 四类归因；只有实现错误允许同协议重做。

## 结束后：故事结算

把 R1 骨架复制为 `paper/STORY_SPINE_R1_<date>.md` 归档；按台账在"结算"节选定一个分支并写证据 ID；填落实决定；`paper/VENUE_PROFILE.md` 写决定与理由。规则见 `paper-storytelling/references/story-spine-template.md`。

## 复核

关键结论登记复核者；复核者实际查证据：读回执、重算、对照独立实现或原始材料，不是看一眼。
