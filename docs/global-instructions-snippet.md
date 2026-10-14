# 全局指令建议：Research stage lock

把下面这段粘进你的全局 CLAUDE.md 或 AGENTS.md，Claude 与 Codex 可共用一份。它以 `research-pipeline` 为总入口，`innovation-explore` 保持 R0 的阶段锁；仓库内的 [AGENTS.md](../AGENTS.md) 是同一份约定的项目级版本。

```markdown
## Research stage lock
- 任何论文项目先读 `research/STATE.md`；没有就用 $research-pipeline 建骨架并判定阶段。阶段由产出文件和门槛决定，不由对话决定。已有自己文件布局的项目只建 STATE.md 与 PROGRESS.md，把现有路径登记进阶段产出索引，不改名、不建空模板。
- 不跳阶段：R2 协议之前要有 R1 的 FRAMING 与 STORY_SPINE；R4 写作之前要有 R3 的台账；R5 投稿前要有 L3 评审。后一阶段发现前一阶段的问题就回退，不打补丁。
- 骨架在实验之前写成立与不成立两个分支；换 venue 只改读者与收获，不改比较、规则和主张强度；实验已做完的项目走事后入口，时点如实。
- 创新点探讨（R0）只用 $innovation-explore，由我自己输入 /innovation-explore 触发；它"严禁输出实验方案 / 论文结构"的阶段锁照旧。
- 每个阶段结束停下等我判断。训练、API、真实数据、保护集、投稿、外发各需我的具体授权，阶段状态不能推导授权。
```

为什么把总入口放进全局锁：

- 只锁 R0 的指令防得住"过早进入 framing"，防不住"实验做完才补主线"和"写作阶段给前面的问题打补丁"，而这两条是最常见的流程问题（见 [CONTEXT.md](../CONTEXT.md) 的起因）。
- `research-pipeline` 只判定阶段、核对门槛、路由与记录，不产出内容，放在全局锁里不会抢各阶段 skill 的工作。
- `innovation-explore` 的规则一字不变；它退出时把 R0 门槛写进 `research/STATE.md`，再由 `research-pipeline` 核对后进入 R1。
