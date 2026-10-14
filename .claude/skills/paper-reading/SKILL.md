---
name: paper-reading
description: Graduate-level academic paper reading and literature analysis. Use when the user asks the agent to read, explain, critique, compare, or turn one or more papers, PDFs, abstracts, links, paper sections, reading notes, or literature reports into Chinese/English analysis, full paper analysis reports, related work notes, seminar explanations, review-style comments, or an HTML literature dashboard. The skill requires long-form, evidence-bounded paper解析 reports with detailed problem, method, experiment, limitation, and reuse analysis; it explicitly rejects brief bullet summaries and raw Markdown dumps. 中文触发短语：精读这篇论文、讲清楚它的方法和实验、解析这几篇 PDF 并比较、写相关工作笔记、组会讲解、审稿式评价、文献分析 HTML 页面。
---

# Paper Reading

## Objective

Read papers so a graduate student can restate, question, reuse, and cite them. Do not produce a generic summary or a short note. The default deliverable is a complete paper analysis report: a coherent article with paragraphs, tables only where they help comparison, and explicit evidence boundaries. Reconstruct three chains:

1. Problem chain: why the paper exists, what gap it claims, and why the gap matters.
2. Mechanism chain: how the method works, what each module receives and outputs, and why each module exists.
3. Evidence chain: what experiments or textual evidence support, what remains only a claim, and where the conclusion stops.

Keep every judgment tied to source text, tables, figures, formulas, experiments, or explicitly marked inference. If the available source is too thin for a full analysis, still write a complete "provisional report" that explains exactly what cannot be verified and why the missing material matters.

## Completeness Contract

A valid paper-reading output must read like a full analysis report, not a checklist. Follow these density rules unless the user explicitly asks for a short answer:

- Each major section must contain explanatory paragraphs. Do not let a section end after one or two short sentences.
- Use bullets and tables only to organize modules, evidence, baselines, or questions. After each important table, add a paragraph explaining how to read it.
- For a full paper, cover at least: research context, exact gap, claim versus evidence, method pipeline, module necessity, assumptions, experiment logic, dataset/baseline/metric fit, conclusion strength, limitations, relation to the user's work, and review questions.
- If formulas, algorithms, ablations, baselines, or metrics are absent from the available evidence, create an explicit "missing evidence" paragraph. Do not silently skip them.
- Avoid note-like fragments such as "方法有效。实验充分。局限是...". Explain mechanism and evidence in connected prose.
- Do not pad with generic background. Expansion must be anchored to the paper, the available source, or the user's research question.

## Evidence Rules

- Do not invent experiments, datasets, baselines, metrics, numbers, ablations, equations, citations, claims, or conclusions.
- Distinguish `author claims`, `confirmed from text`, and `assistant inference`.
- If only title/abstract/metadata is available, say the analysis is provisional and do not assert method or experiment details absent from the source.
- If the full text is unavailable, mark the item as `metadata-only`, `abstract-only`, or `closed access` and list what still needs verification.
- Do not call an improvement "significant" unless the paper reports statistical significance or concrete values that justify the wording.
- Do not convert correlation into causation, local results into universal conclusions, or benchmark performance into deployment safety.
- Do not say "important", "effective", "sufficient", "novel", or "SOTA" without the concrete evidence and comparison scope.
- When using external sources, prefer primary sources: the paper PDF, official proceedings, arXiv, publisher pages, artifact repositories, or official benchmark pages.

## Source Handling

Before analysis, identify what evidence is available:

| Evidence level | Allowed claims |
|---|---|
| Full paper | Analyze problem, method, experiments, limitations, and writing, while still citing boundaries. |
| Section/table/figure only | Analyze only that fragment and state which sections are missing. |
| Abstract only | State the claimed problem, claimed method, and claimed evidence; do not confirm contribution strength. |
| Metadata only | Record bibliographic relevance and required follow-up; do not infer technical content. |
| User notes only | Treat notes as user-provided claims unless source text confirms them. |

If multiple PDFs, reports, or notes already exist locally, reuse them before downloading or re-extracting. Preserve uncertainty from the source artifacts.

## Single-Paper Workflow

### 1. Locate the Paper

Classify the paper type because reading priorities differ:

| Type | Primary question |
|---|---|
| Method paper | What new mechanism is added, and is it isolated by ablation? |
| Dataset/benchmark paper | Does the dataset or protocol actually measure the target ability? |
| Analysis paper | Are variables controlled, and are conclusions overextended? |
| Application paper | Does the new setting create a new research problem or mainly an engineering transfer? |
| Theory paper | Are assumptions realistic, and where do the results apply? |
| Survey paper | Is the taxonomy coherent, and what routes or failures are missing? |
| Negative-result paper | Are failure causes isolated well enough to rule out implementation artifacts? |

Then answer five orientation questions, but do not stop there. These are only the opening of the report:

1. Research object: what object, field/task, and concrete problem.
2. Problem/gap: what existing approach fails, in which scenario, and with what consequence.
3. Core claim: what mechanism/data/theory/analysis is claimed to improve, explain, or evaluate what target.
4. Contribution split: what the authors claim versus what the available text actually confirms.
5. Importance: what upstream/downstream/evaluation/deployment/theory step is blocked if the problem remains unsolved.

### 2. Rewrite the Abstract

Break the abstract into background, pain point, method, and result. Then produce:

- One-sentence version: "This paper targets X, proposes Y, and evaluates/founds Z under W."
- Researcher version: state the problem logic, method mechanism, implicit assumption, main validation target, and evidence dependency.

### 3. Reconstruct Introduction and Related Work

For the introduction, extract:

- Background premise: what the authors assume the reader accepts.
- Gap: whether it is task-level, method-level, data-level, evaluation-level, or theory-level.
- Motivation: why the proposed mechanism could plausibly address the gap.
- Contribution sentence cleanup: translate promotional claims into verifiable statements and list required evidence.

For related work, build a route table:

| Route | Representative works | Shared idea | Limitation | Relation to this paper |
|---|---|---|---|---|

Do not invent missing citations. If the related work section is absent, say that omission prevents judging whether a route was ignored.

### 4. Decompose the Method

Give a plain-language pipeline:

> Input X goes through module A, then module B, and outputs Y. Module A handles ..., module B handles ...

For each major module, use a table, then explain the table in prose:

| Module | Input | Output | Subproblem solved | Why needed | Evidence of necessity |
|---|---|---|---|---|---|

For formulas, do not skip notation. If formula extraction is unavailable, say so explicitly and describe what must be checked in the original paper:

1. Quote or reference the formula location when available.
2. Explain each symbol.
3. Explain each term.
4. Translate the formula into natural language.
5. State what assumption or tradeoff it encodes.

For algorithms, rewrite as human-readable pseudocode with the purpose of each step. Then identify the key design decision, not just the sequence of steps. If no algorithm block is available, explain the method flow at the same level of operational detail that the source supports.

Always list implicit assumptions, for example: external knowledge is reliable, auxiliary tasks share useful representations, negative samples reflect semantic contrast, logs represent normal access, or the benchmark captures real-world risk.

### 5. Read Experiments as Evidence

Do not read experiments as rankings. Map each experiment to the claim it tests:

| Experiment | Research question | Object tested | Key metric | Supported claim | Evidence strength |
|---|---|---|---|---|---|

Then check:

- Datasets: what they measure, scale if reported, and whether they match the claimed problem.
- Baselines: whether they include the strongest relevant, simple strong, same-budget, and current methods.
- Metrics: what each metric measures and what it cannot measure.
- Main results: where improvement appears, whether it is consistent, whether any setting drops, and whether significance/intervals are reported.
- Ablations: which module necessity is isolated; absent ablation means necessity is not proven.
- Case studies: whether failures and representative cases are shown or only successful examples.

Use limited conclusion wording:

> The result supports the narrower claim that ... under ...; it does not prove ... because ...

### 6. Grade Conclusions and Limits

Separate paper conclusions into:

| Strength | Meaning | What this paper supports |
|---|---|---|
| Strong | Direct evidence, controlled setup, consistent support | ... |
| Medium | Some support but setting-dependent | ... |
| Weak | Motivation, speculation, or local observation | ... |

List both author-acknowledged limitations and reader-inferred limitations. Reader-inferred limitations must be grounded in missing baselines, metrics mismatch, data scope, uncontrolled variables, costs, reproducibility gaps, or deployment assumptions.

### 7. Judge Innovation

Score or describe innovation across four dimensions, with reasons:

| Dimension | Judgment | Reason |
|---|---|---|
| Problem innovation | Strong/Medium/Weak | ... |
| Method innovation | Strong/Medium/Weak | ... |
| Empirical innovation | Strong/Medium/Weak | ... |
| Theoretical innovation | Strong/Medium/Weak | ... |

End with: "The main increment is closer to X than Y." Keep this as a reading judgment, not a paper fact.

## Required Output Structure

For a normal full-paper reading, use the following structure, but write each section as long-form analysis. Section titles are not a substitute for content.

## 1. 论文一句话定位
## 2. 论文要解决的问题
## 3. 核心贡献拆解
### 作者声称的贡献
### 实际可确认的贡献
## 4. 方法揉碎讲解
### 总体流程
### 模块拆解
### 公式 / 算法解释
### 隐含假设
## 5. 实验逻辑
### 实验在验证什么
### 数据集与指标
### Baseline 是否充分
### 消融实验说明了什么
## 6. 论文真正证明了什么
### 强结论
### 中等结论
### 弱结论
## 7. 局限与风险
## 8. 可复述版本
### 10 秒版
### 1 分钟版
### 组会版
## 9. 对我自己研究的可迁移点
## 10. 审稿式评价
### Strengths
### Weaknesses
### Questions

Minimum content expectations for a full paper report:

- `论文要解决的问题`: explain the research background, why existing work is insufficient, and which layer the gap belongs to.
- `方法揉碎讲解`: include a pipeline, module table, module necessity analysis, assumptions, and formula/algorithm status.
- `实验逻辑`: discuss what each known experiment validates, what datasets/baselines/metrics can and cannot prove, and whether ablation/case studies isolate the mechanism.
- `论文真正证明了什么`: separate strong, medium, and weak conclusions in prose, not only as labels.
- `局限与风险`: include both author-acknowledged limits and reader-inferred limits, with their effect on the conclusion.
- `对我自己研究的可迁移点`: say where the paper can be cited or reused and where it cannot be used as evidence.

If the user wants a shorter answer, output at least:

1. 一句话定位
2. 问题与 gap
3. 方法核心机制
4. 实验证据是否支撑主张
5. 局限与可用价值

## Multi-Paper Mode

When analyzing multiple papers, do not summarize each independently and stop. Compare them:

| Paper | Problem definition | Method route | Core assumption | Evidence | Limitation | Useful for user's work |
|---|---|---|---|---|---|---|

Then identify relationships:

- Same problem, different methods.
- Successive work or extension.
- Method versus benchmark/evaluation.
- Theory versus empirical evidence.
- Mutual challenge or contradiction.
- Parallel work in different scenarios.

End with a reading route:

> These papers are not merely parallel. Paper A defines ..., Paper B operationalizes ..., Paper C tests/extends/questions ..., forming a route from ... to ... to ...

## HTML Literature Dashboard Mode

When the user asks for an HTML literature analysis page, make the page information-complete rather than promotional. The page must render Markdown into readable HTML typography; never display raw Markdown as the main report body. Include:

- Evidence summary: number of papers, full PDFs, partial sources, closed-access items, and unverified items.
- Search and filters by research route, evidence level, paper type, or method family.
- A comparison matrix with problem, method, evidence, limitation, and use for the user's research.
- Per-paper cards with: one-sentence location, problem/gap, method mechanism, experiment/evidence, confirmed contribution, limits, transferable use, review questions, and source links.
- A full rendered analysis article for each paper, not just a compressed card summary. Use headings, paragraphs, tables, lists, and article typography.
- Evidence badges such as `全文 PDF`, `摘要-only`, `closed access`, or `待核实`.
- Subjective scores only if labeled as reading judgments, not facts.
- Visual assets such as PDF previews when available; do not use decorative visuals that obscure content.

For closed-access or incomplete papers, show the missing evidence explicitly inside the card instead of hiding the item.
For long report bodies, use a readable article layout with line length control, heading hierarchy, table styling, and collapsible navigation if needed. Do not leave fenced Markdown, raw heading markers, or unstyled note dumps visible to the reader.

## User Intent Priority

- If the user says "看不懂", explain concepts and method first; postpone critique.
- If the user says "写 related work", position relationships among papers before writing prose.
- If the user says "审稿", focus on claim-evidence alignment.
- If the user says "讲实验", explain what each experiment validates.
- If the user says "创新点", split problem, method, empirical, and theory innovation.
- If the user says "能不能用", judge which part of the user's argument the paper can support and what it cannot support.

## Prohibited Answers

Do not output:

- Generic praise such as "本文提出了一种新颖有效的方法，并取得优异结果".
- A report made mostly of short bullet points or one-sentence sections.
- Raw Markdown dumps in HTML dashboards.
- "实验充分证明" without direct evidence and scope.
- SOTA claims without paper tables or external primary-source verification.
- "显著提升" without statistical significance or concrete reported values.
- Related-work prose that only stacks summaries without relationships.
- A final "如果你需要，我可以继续..." when the requested reading output is already complete.
