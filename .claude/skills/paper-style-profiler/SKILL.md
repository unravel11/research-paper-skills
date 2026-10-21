---
name: paper-style-profiler
description: "Discover the strongest published style-anchor papers already present in the current academic repository, select a complementary three-to-five-paper corpus, extract and save its aggregate language style, refresh stale profiles, audit a manuscript against the saved contract, or apply that contract while preserving claims and terminology. Use for repository-specific paper writing and revision; not for literature review, copying an author's sentences, authorship-detector evasion, or unsupported claim strengthening. 中文触发短语：从文献库里挑几篇优秀论文提炼文风或风格合同、写作合同，按已保存的风格改写这一节但不改数字和结论，刷新文风画像，审一下这稿和范文的语言差距。"
---

# Paper Style Profiler

Build a repository-local, reusable English-language style contract from published full-text papers that fit the current manuscript. Treat the corpus as evidence about language choices, not as text to copy and not as authority for scientific claims. The bundled metrics helper is English-specific; do not apply its lexical metrics to another language without a validated analyzer for that language.

## Non-negotiable boundaries

- Separate **language style** from argument structure. Subjects, voice, verbs, tense, modality, sentence construction, connectives, punctuation, and paragraph rhythm belong here. Section order, contribution count, method design, experiment design, and figure layout do not.
- Aggregate three to five complementary papers. Never imitate one author sentence by sentence, reproduce distinctive wording, or make a near paraphrase.
- Preserve the target manuscript's facts, numbers, polarity, uncertainty, causal strength, scope, baselines, citations, terminology, and locked spans. Style may make a claim clearer; it may not make it stronger.
- Treat measurements as descriptive evidence, never quotas, acceptance predictors, quality scores, AI scores, or authorship classifications.
- Do not optimize for detector evasion. If that is requested, decline that objective and offer a conventional academic-prose audit for formulaic, repetitive, vague, or legalistic writing.
- Use repository papers by default. Browse or add external papers only when the user explicitly requests it or governing instructions require current external verification.

## Choose the operating mode

Inspect the repository and any existing style state before choosing a mode:

- `STATUS`: report corpus, anchors, hashes, profile age, target coverage, and stale conditions without writing.
- `DISCOVER_AND_EXTRACT`: no valid saved profile exists, or the user asks to build one from the repository.
- `REFRESH`: candidate papers, selected anchors, venue, target manuscript, or hashes changed.
- `AUDIT`: compare manuscript language with the saved profile; do not revise unless requested.
- `WRITE_OR_REVISE`: draft or minimally revise specified manuscript text using a valid saved contract.

If the request is ambiguous, prefer `AUDIT` over mutation. A saved profile does not authorize editing the manuscript.

## Recognize existing project style work

Before creating a new bundle, search scoped project locations for an existing corpus contract, language profile, metrics, builder script, or project validator. Treat it as `LEGACY_PROFILE_FOUND`, not as absent state. It may be adopted only when the selected full texts are identified and hash-pinned, selection rationale is recorded, the artifact covers the actual language dimensions in this skill, source sentences are not reused, and the repository's own validator still passes.

Do not silently rewrite a legacy layout into `.paper-style/`. In `STATUS`, report whether it is usable under project governance and which refresh operations are impossible without the original full texts. In `REFRESH`, require verifiable source files; notes and metrics alone are not a substitute for the corpus. Convert to the standard bundle only when conversion is part of the requested scope.

## Resolve authority before analysis

1. Find and read all applicable repository instructions, especially `AGENTS.md` or `CLAUDE.md`.
2. Identify the authoritative checkout or remote worktree, repository root, branch, HEAD, status, target manuscript, target venue/field, and stated claim ceiling.
3. Follow repository-specific source-of-truth and commit rules. Do not write to a disposable mirror when the repository declares another checkout authoritative.
4. Identify the bundle location. Use an existing configured location if present; otherwise propose `.paper-style/` and state that path before writing.
5. Keep raw PDF text in an explicit temporary directory outside the repository. Never place extracted source text in the saved bundle.

If authority or the target manuscript is materially ambiguous, stop with `BLOCKED_AUTHORITY_AMBIGUOUS` and name the missing decision.

## Discovery and extraction workflow

### P0 — Resolve the project

Record the authority, target, venue/genre, scientific claim ceiling, and applicable exclusions. Do not infer these from filenames alone.

### P1 — Freeze the candidate inventory

Use scoped repository search (`rg --files` first) and avoid dependencies, caches, generated builds, virtual environments, raw datasets, and unrelated archives. The helper `scripts/inventory_papers.py` may inventory PDFs and derive hashes and extraction-quality signals without retaining source text. Invoke it as `python3 scripts/inventory_papers.py <repo-root> --scope <relative-dir> --output <bundle>/CORPUS-INVENTORY.json` (`--scope` is repeatable; add `--include-ignored` to walk Git-ignored paths). It discovers `.pdf` files only, and its page counts and text-quality signals rely on the optional `poppler-utils` binaries `pdfinfo` and `pdftotext`; when they are absent the extraction fields degrade to `tool_unavailable` rather than failing.

Classify candidates as one of:

- external published full-text paper;
- current or prior manuscript by the project authors;
- slide, report, thesis, review response, or non-paper material;
- duplicate or incomplete/unreadable source;
- unresolved.

Only the first class is eligible by default. Freeze the inventory before close language reading so attractive sentences cannot silently change the sampling frame. Follow `references/discovery-selection.md`.

### P2 — Freeze three to five complementary anchors

Score eligible papers using the documented rubric, then select for both fit and complementarity. Cover at least these rhetorical roles when the repository permits:

- empirical Results and evidence interpretation;
- method, mechanism, or system description;
- Discussion, limitations, or claim-boundary language.

A high total score does not override a claim-ceiling conflict. Record every selected anchor, primary role, score, selection basis, hash, and material exclusion. If fewer than three suitable full texts remain, set `INSUFFICIENT_REPOSITORY_STYLE_CORPUS`; do not pad the corpus with the current manuscript, duplicate versions, or weakly related papers.

### P3 — Extract the language layer

Convert selected PDFs to temporary plain text with a deterministic extractor. Hash the original PDFs, note extraction coverage, and exclude references from measurement where feasible. The helper `scripts/profile_language.py` produces quote-free descriptive metrics; it does not replace close reading. Invoke it as `python3 scripts/profile_language.py --paper A1=<tmp>/a1.txt --paper A2=<tmp>/a2.txt ... [--target T=<tmp>/target.txt] --output <bundle>/metrics.json`, where each `--paper` names a selected anchor ID and its temporary plain-text path (for example from `pdftotext`, which is optional `poppler-utils` software).

Extract the dimensions in `references/language-profile.md`, including:

- grammatical subjects and research agency;
- active/passive balance and first-person use;
- action, evidence, interpretation, comparison, and boundary verbs;
- tense, aspect, modality, and hedging;
- sentence length, clause chaining, opening patterns, and punctuation;
- discourse relations and paragraph opening/development/ending rhythm;
- section-specific language for Introduction, Method, Results, Discussion, and Limitations;
- numerical comparison, uncertainty, negative-result, and scope-limiting language.

For every qualitative rule, state whether it is shared, role-specific, or paper-specific. Save no long quotations and no reusable source sentences.

### P4 — Save the reusable bundle

Write the artifacts and machine state defined in `references/repo-bundle-contract.md`. The complete bundle contains:

- `STYLE-STATE.json`
- `CORPUS-INVENTORY.json`
- `SELECTION-REPORT.md`
- `LANGUAGE-STYLE-PROFILE.md`
- `WRITING-CONTRACT.md`
- `metrics.json`
- `TARGET-GAP-AUDIT.md` when a target audit was performed

Run `scripts/validate_style_bundle.py` before calling the profile usable. A mechanically valid bundle proves schema and traceability only, not that the selected papers are scientifically optimal or that revised prose is publication-ready.

### P5 — Audit the target

Compare the manuscript with the aggregate and section-specific contract. Report concrete gaps, locations, confidence, and likely effect. Distinguish:

- a genuine language mismatch;
- a project-required claim boundary;
- a deliberate terminology choice;
- an extraction or genre artifact.

Do not rewrite merely to make numeric rates resemble the corpus. Save the audit only when requested or when it is part of a full extraction run.

### P6 — Write or revise

Load and verify the saved state first. If anchor or target hashes are stale, refresh or report the stale condition before editing. Apply `references/apply-style.md` and make evidence-sized changes. For a manuscript-wide task, audit terminology and recurring patterns across the whole document after local edits.

## Refresh rules

Refresh rather than silently reuse when any of these changes:

- an anchor PDF hash or path;
- the eligible candidate inventory materially;
- target venue, research genre, or manuscript role;
- target manuscript identity;
- selection rationale or claim ceiling;
- extraction tooling in a way that changes measurements.

A changed target hash alone normally requires a new target audit, not reselection of anchors. Record the reason and retain prior state through version control; do not overwrite provenance invisibly.

## Validation and handoff

Before finishing:

1. validate JSON and the bundle schema;
2. verify every selected hash against the source PDF;
3. confirm three to five unique external anchors and their complementary roles;
4. scan the bundle for raw extracted text, long source quotations, private absolute paths, and unsupported quality claims;
5. distinguish completed extraction, human judgment still needed, and unverified manuscript quality;
6. when repository rules require it, add the project activity entry and commit/push from the authoritative checkout.

Report in plain language: what was selected, why those papers, where the contract was saved, what language patterns were found, what was deliberately not inherited, what validation passed, and what remains a human judgment.
