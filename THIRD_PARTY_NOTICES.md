# 第三方 skill 的来源与许可

本仓库随附六个第三方 skill。`drawio-skill`、`task-forest`、`session-handoff-prompt` 与上游锁定提交逐字节相同；`scientific-visualization`、`publication-chart-skill`、`academic-humanizer` 相对上游有小改，改动逐条列在各自小节；锁定的上游提交记在 [external-skill-locks.md](.claude/skills/paper-writing-orchestrator/references/external-skill-locks.md)。它们都以 MIT 许可发布。MIT 要求副本附带版权声明与许可声明，因此这里全文收录；核对日期 2026-10-14。

| skill | 上游 | 提交 | 版权 |
|---|---|---|---|
| `scientific-visualization`（有小改） | K-Dense-AI/scientific-agent-skills | `48dc1cf1…` | 2025 K-Dense Inc. |
| `publication-chart-skill`（有小改） | Galaxy-Dawn/claude-scholar | `2f7766fd…` | 2026 Gaorui Zhang |
| `drawio-skill` | Agents365-ai/drawio-skill | `2ee141e0…` | 2026 Agents365-ai |
| `academic-humanizer`（有小改） | dongshuyan/compass-skills | `1b2e556c…` | 2026 COMPASS Skills contributors |
| `task-forest` | dongshuyan/compass-skills | `1b2e556c…` | 2026 COMPASS Skills contributors |
| `session-handoff-prompt` | dongshuyan/compass-skills | `1b2e556c…` | 2026 COMPASS Skills contributors |

## scientific-visualization

- 目录：`.claude/skills/scientific-visualization/`
- 上游：[K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)，路径 `skills/scientific-visualization`，提交 `48dc1cf173f01aea114a62d634066f6b272aaaf1`
- 许可：MIT，见上游仓库根目录的 `LICENSE.md`
- `scientific-visualization` 相对上游 `48dc1cf1` 的改动：头部版本 1.1 改 1.2，`compatibility` 字段移到正文末尾的 Environment compatibility 段；新增一条规则，不按 ours / proposed / baseline 这类方法角色分配好坏颜色；新增 Exact labels 一条；新增 `references/real_world_patterns.md`（三个有边界的实践模式，附来源与不得复制的声明）并在正文引用；新增 `evals/evals.json`（8 个用例）。

```
MIT License

Copyright (c) 2025 K-Dense Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## publication-chart-skill

- 目录：`.claude/skills/publication-chart-skill/`
- 上游：[Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar)，路径 `skills/publication-chart-skill`，提交 `2f7766fd541a723d4ddc6230b3277f948d61b093`
- 许可：MIT，见上游仓库根目录的 `LICENSE`
- `publication-chart-skill` 相对上游 `2f7766fd` 的改动：版本 0.2.0 改 0.2.1 并移到 metadata 下；SKILL.md 新增 Responsibility boundary 一节，写明与 scientific-visualization 的分工；`references/workflow.md` 新增第 6 步（图交给 scientific-visualization 做完整性与导出检查）和 Responsibility and handoff 表。

```
MIT License

Copyright (c) 2026 Gaorui Zhang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## drawio-skill

- 目录：`.claude/skills/drawio-skill/`
- 上游：[Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill)，路径 `skills/drawio-skill`，提交 `2ee141e0ff183ce76dc405370aeb142c6961aa45`
- 许可：MIT，见上游仓库根目录的 `LICENSE`
- 运行时依赖 draw.io 桌面版的命令行（可选 Graphviz），见其 SKILL.md

```
MIT License

Copyright (c) 2026 Agents365-ai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## academic-humanizer、task-forest、session-handoff-prompt

- 目录：`.claude/skills/academic-humanizer/`、`.claude/skills/task-forest/`、`.claude/skills/session-handoff-prompt/`
- 上游：[dongshuyan/compass-skills](https://github.com/dongshuyan/compass-skills)，路径 `skills/<同名>`，提交 `1b2e556ce6f293ba12e95e18d51995d6a969d52f`
- 许可：MIT，见上游仓库根目录的 `LICENSE`
- `task-forest` 与 `session-handoff-prompt` 未改动。`academic-humanizer` 相对上游有以下改动：description 加了中文触发短语；SKILL.md 加了"每个 reference 每次任务只读一遍"和"先读 `references/user-writing-defaults.md`"两段，并把 `references/examples.md` 改为按需读取（examples.md 开头说明同步改）；新增 `references/user-writing-defaults.md`（学术写作默认语气）；`scripts/metrics.py` 的候选输出多了一个 `status` 字段。

```
MIT License

Copyright (c) 2026 COMPASS Skills contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 只引用、未随附的 skill

`paper-writing-orchestrator` 的路由表还提到几个不在本仓库里的 skill：`$pdf` 是 Anthropic 的文档 skill，按 Anthropic 自己的许可分发，不在这里转载；`$jupyter-notebook`、`$academic-paper-ppt`、`$review-paper` 是可选路由；`task-forest` 提到的 `$task-clarifier` 是 compass-skills 里的另一个 skill，也未随附。没有安装时对应的路由跳过。
