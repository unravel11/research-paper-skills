# R3 实验执行：按协议跑，结果进台账

执行本身用项目自己的运行 skill（ssh / GPU / 队列脚本）；本 reference 只规定执行的纪律和产出。

## 开始前

- 核对协议哈希与当前脚本哈希一致（`python3 <skill_dir>/scripts/check_gates.py <项目> --stage R2` 会逐行比对协议里的哈希表）；不一致先记差异，不改协议。
- 核对授权：这次运行属于协议里哪条授权；训练 / API / 真实数据分别核。
- 登记 `PROGRESS.md` 任务行：任务 ID、执行者、范围、完成条件。
- 远端工作目录与输出路径按项目的 START_HERE / GPU_ACCESS 规则；本地不落原始数据。

## 运行中

- 每个 cell（配置 × 种子 × 集合）跑完写完成标记；失败写失败回执并保留，不删。
- 重跑只针对失败的 cell，并记录原因（例如内存错误），不借机重跑已成功的 cell。
- 不看 test 结果改配置。dev 只能做协议允许的三件事：完成性检查、温度 / 阈值拟合、按协议决定进入 test 的配置。
- 中途想加的分析一律先写进"事后分析"节，再跑。

## 结束后：RESULT.md

`reports/<run>/RESULT.md` 固定包含：

1. 协议引用与哈希核对结果。
2. 完成标记统计（例如 22/22），失败与重跑清单。
3. 每个 RQ 的判定：数值、区间、规则、结论（成立 / 不成立 / 不能判定）。种子表完整列出，不挑选。
4. 事后分析一节：每条标 post hoc、触发原因、是否影响主张。
5. 输出文件清单（`outputs/`），每个正文可能引用的数字都能指到文件。
6. 本地与远端同步状态；未核实项。

骨架如下（`check_gates.py` 检查"判定"、"事后分析"、哈希核对三节是否存在）：

```markdown
# RESULT：<run 名>

## 协议与哈希核对
- 协议：experiments/PROTOCOL_<date>.md（冻结哈希：）
- 脚本哈希与协议一致：是 / 否（差异：）

## 完成统计
- cell 完成 <n>/<N>；失败回执：…；重跑：…（原因）

## 结果中性检查
| 检查 | 通过标准 | 结果 | 影响的 RQ |
|---|---|---|---|

## 判定
| RQ | 规则（引自协议） | 数值与区间 | 种子表 | 结论（成立 / 不成立 / 不能判定） | 证据 ID |
|---|---|---|---|---|---|

## 事后分析（post hoc）
| 分析 | 触发原因 | 结果 | 是否影响主张 | 证据 ID |
|---|---|---|---|---|

## 输出文件清单
- outputs/…

## 同步与未核实
- 本地 / 远端：
- 未核实：
- 复核者与复核结果：
```

## 台账

- 文件在 `paper/ledger/`：`evidence_inventory.csv`（或 `.json`）每条结果一行，状态按 orchestrator 合同（`VERIFIED_CURRENT` / `CONTROLLED_OR_RETROSPECTIVE` / `EXPLORATORY_OR_CANDIDATE` / `SUPERSEDED_OR_INVALID` / `MISSING_OR_UNRESOLVED`），`output_file` 指到输出文件；`claim_ledger.csv` 每条可写进论文的主张一行，允许强度与禁止升格写清，状态 `SUPPORTED` / `WEAKEN` / `ABSTAIN` / `REMOVE_FROM_CURRENT_CHAIN`。列定义见项目骨架 `paper/ledger/README.md`。
- 有脚本就从输出文件生成台账，不手写；长期项目存 JSON 并校验。R4 的 orchestrator S1 直接继承这两张表。

## 结果不如预期

先归类再动手：实现错误、数据问题、设计缺陷、真实阴性，证据要求和允许的动作见 [when-results-disappoint.md](when-results-disappoint.md)。只有实现错误允许同协议重跑；真实阴性走骨架的不成立分支。

## 结束后：故事结算

RESULT.md 写完后，把 `paper/STORY_SPINE.md` 的 R1 版本复制为 `paper/STORY_SPINE_R1_<date>.md` 归档，再在 STORY_SPINE.md 的“结算”节按台账选定分支，并在 `paper/VENUE_PROFILE.md` 填“决定”。这是 R3 到 R4 的门槛之一。

## 复核

关键结论登记复核者。复核者至少做：只读取回执核对完成标记、用预登记脚本重算一次、与独立实现对比一次（如 bootstrap）。复核结果写进 RESULT.md 与 PROGRESS.md，完成前状态是"待复核"。
