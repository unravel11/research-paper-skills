# paperforge（Codex 入口）

本仓库是一套论文工作流 skill。先读 README.md 与 CONTEXT.md。Claude Code 读 CLAUDE.md，它指向本文件，两边是同一份约定。

## 研究阶段锁

- 任何论文项目先读 `research/STATE.md`；没有就用 `$research-pipeline` 建骨架并判定阶段。阶段由产出文件和门槛决定，不由对话决定。已有自己文件布局的项目只建 STATE.md 与 PROGRESS.md，把现有路径登记进阶段产出索引，不改名、不建空模板。
- 不跳阶段：R2 协议之前要有 R1 的 FRAMING 与 STORY_SPINE；R4 写作之前要有 R3 的台账；R5 投稿前要有 L3 评审。后一阶段发现前一阶段的问题就回退，不打补丁。
- 骨架在实验之前写成立与不成立两个分支，协议写结果中性检查；换 venue 只改读者与收获，不改比较、规则和主张强度。实验已做完的项目走事后入口，时点如实。
- 创新点探讨（R0）只用 `$innovation-explore`，由用户自己输入 `/innovation-explore` 触发（它设了 disable-model-invocation）；它"严禁输出实验方案 / 论文结构"的阶段锁照旧。
- 每个阶段结束停下等用户判断。训练、API、真实数据、保护集、投稿、外发各需用户的具体授权，阶段状态不能推导授权。

## 约定

- skill 位于 `.claude/skills/<name>/SKILL.md`；Codex 使用时运行 `./install.sh` 链接到 `~/.codex/skills`。
- 语言按用途分：要用户拍板的 skill（流程、方向、framing、故事、评审）正文用中文；直接操作英文稿件或包着第三方工具的 skill（humanizer、style-profiler、orchestrator、图表）正文用英文。术语不翻（framing、post hoc、venue、claim ceiling）；状态值、文件名、脚本解析的小节标题是常量，不随语言改。
- 触发靠 `description`：每个自写 skill 的 description 同时写中英文触发短语；保持 SKILL.md 头部 `name` / `description` 格式，单行 description 里不出现英文冒号加空格。第三方 skill 的头部不动。
- 评审只有一个 skill：`paper-review`。venue 之间的差别写进它的 `references/venues/<缩写>.md`，不再为某个期刊单独建评审 skill。
- 第三方 skill（`scientific-visualization`、`publication-chart-skill`、`drawio-skill`、`academic-humanizer`、`task-forest`、`session-handoff-prompt`）以上游锁定提交为基线，锁定版本记在 `paper-writing-orchestrator/references/external-skill-locks.md`，版权与已有的小改逐条记在 `THIRD_PARTY_NOTICES.md`；不再新增改动，需要调整它们的行为时写在调用方（orchestrator、research-pipeline）。
- 模板只放一处：各阶段的文件骨架归产出它的 skill（FRAMING 在 paper-framing，骨架在 paper-storytelling，协议与 RESULT 在 research-pipeline 的 reference）；跨 skill 的文件（STATE、PROGRESS、FIGURE_PLAN、台账表头）在 `research-pipeline/assets/project-skeleton/`。
- 新增规则先写进 CONTEXT.md 的"固化进流程的规则"，再落到对应 SKILL.md。
- 改完运行 `python3 scripts/validate_skills.py`。
- 不在任何 skill 中写入私人路径、主机地址、密钥或未公开数据。
