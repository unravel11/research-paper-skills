# Progress

> 任务表与交接记录。Claude 与 Codex 读写同一份；阶段状态只看 research/STATE.md，这里不重复写阶段。

## 任务表

| 任务 ID | 阶段 | 执行者 | 复核者 | 范围 | 完成条件 | 授权出处 | 状态 | 备注 |
|---|---|---|---|---|---|---|---|---|
| T001 | R0 | | | 确定研究设定并写入 docs/innovation-log.md | 用户确认方向、前提条件、已排除方向 | | 待开始 | |

状态取值：待开始 / 进行中 / 待复核 / 完成 / 取消。关键科学结论和大范围改动必须有复核者；复核者实际查证据后才能从"待复核"改为"完成"。

## 交接记录

### {{DATE}} — 项目创建
- 做了什么：用 research-pipeline 的 `init_paper_project.py` 建立项目骨架。
- 证据位置：research/STATE.md
- 未核实项：无
- 下一位从哪开始：R0，调用 $innovation-explore
