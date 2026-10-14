# paper/ledger

R3 结束时由脚本从输出文件生成，R4 只继承、不改写。列与 `paper-writing-orchestrator/references/state-and-ledger-contracts.md` 的合同一致。

- `evidence_inventory.csv`：每条结果一行。`status` 只能是 `VERIFIED_CURRENT` / `CONTROLLED_OR_RETROSPECTIVE` / `EXPLORATORY_OR_CANDIDATE` / `SUPERSEDED_OR_INVALID` / `MISSING_OR_UNRESOLVED`。`output_file` 指到 `reports/<run>/outputs/` 下的文件，正文里的每个数字都要能顺着它找回去。
- `claim_ledger.csv`：每条可以写进论文的主张一行。`status` 只能是 `SUPPORTED` / `WEAKEN` / `ABSTAIN` / `REMOVE_FROM_CURRENT_CHAIN`；`allowed_strength` 写允许的措辞（形容词跟着数字走），`prohibited_upgrade` 写禁止的升格。
- 事后分析的条目在 `supports` 里标 `post hoc` 与触发原因，状态一般是 `EXPLORATORY_OR_CANDIDATE`；不得写成协议内判定。
- 长期项目可以改用 JSON（同名、`.json` 后缀）；`research-pipeline/scripts/check_gates.py` 两种都读。
