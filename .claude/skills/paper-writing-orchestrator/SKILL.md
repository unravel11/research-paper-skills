---
name: paper-writing-orchestrator
description: Orchestrate a multi-stage academic manuscript workflow from authority and evidence intake through argument planning, section drafting, figures and tables, consistency checks, venue review, and final artifact validation. Use when the user asks to start, continue, revise, finish, or manage an end-to-end paper, determine its current stage, or coordinate multiple paper-related skills. Do not use for an isolated paper reading, one paragraph polish, one standalone figure or table, a slide deck, or a PDF-only task unless it is explicitly part of a broader manuscript workflow. 中文触发短语：开始写论文、继续写论文、论文写到哪一步了、稿件阶段、按审稿意见定点修改某一节、离投稿还差什么、协调图表、评审和写作、S0 到 S7。
---

# Paper Writing Orchestrator

Coordinate the paper as a staged, evidence-bounded workflow. A fluent draft is
not evidence, a successful build is not scientific adequacy, and a completed
review is not submission or acceptance.

## Language and scope

- Communicate in the user's language. Preserve the manuscript's requested
  language and disciplinary register.
- Treat the human authors as owners of the research question, scientific
  interpretation, claim strength, author order, disclosures, and submission.
- Do not add experiments, datasets, baselines, citations, results, threat
  models, or contributions that the user did not authorize and supply.
- One-shot generation may produce a clearly labeled outline or disposable zero
  draft. It never creates an authoritative final manuscript.

## Select the operating mode

Choose one mode before acting:

| Mode | Use when | Default action |
|---|---|---|
| `PIPELINE_START` | A new paper or a full writing workflow begins | Resolve authority, evidence, target venue, and claim ceiling |
| `STAGE_DETECT` | The user asks where the paper stands | Inspect only; report the current gate and next admissible step |
| `CONTINUE` | A prior workflow should resume | Verify saved state against current files before continuing |
| `TARGETED_REVISION` | The user names a section, finding, or reviewer issue | Make the smallest evidence-preserving change |
| `SUBMISSION_READINESS` | The manuscript is near submission | Separate scientific, format, artifact, and author-side blockers |

Do not expand a focused request into the full pipeline. Do not edit when the
user asks only for explanation, diagnosis, or review.

When a figure or table is embedded in an active manuscript workflow, a request
to restyle, highlight, reorder, or otherwise change its argumentative emphasis
remains a `TARGETED_REVISION` owned by this orchestrator. Route the rendering
work to the appropriate companion only after applying the manuscript evidence
and claim gates. A truly standalone exploratory figure or table bypasses this
orchestrator as described below.

## Resolve authority before paper work

For a repository-backed paper:

1. Read the applicable `AGENTS.md` or `CLAUDE.md` and repository governance
   files.
2. Resolve the authoritative workspace, manuscript line, branch, HEAD, and
   working-tree state before editing.
3. Follow any required connection or repository-specific skill. Never replace a
   prescribed route with an improvised remote command.
4. Preserve unrelated changes. Do not edit archives, deprecated paper lines, or
   generated outputs when an editable source is authoritative.

For a file-only paper, identify the editable source, supplied evidence bundle,
target venue, and intended output. If competing versions exist, stop and ask
which is authoritative.

## Use the stage gates

The workflow has eight monotonic stages:

1. `S0_AUTHORITY_RESOLVED`
2. `S1_EVIDENCE_LOCKED`
3. `S2_ARGUMENT_LOCKED`
4. `S3_SECTION_DRAFTED`
5. `S4_MANUSCRIPT_INTEGRITY_CHECKED`
6. `S5_VENUE_REVIEWED`
7. `S6_ARTIFACT_VERIFIED`
8. `S7_SUBMISSION_READY`

These names denote completed gates. When manuscript authority is not yet
resolved, report `PRE_S0` with `S0 gate unmet`; do not label the paper
`S0_AUTHORITY_RESOLVED` or create a state file that claims that gate has passed.

Read [stage playbook](references/stage-playbook.md) when starting, detecting, or
advancing a stage. Do not claim a later stage unless every earlier gate has
current evidence. `SUBMITTED` and `ACCEPTED` are external states and are never
inferred by this skill.

For long-running work, use the optional state contract in
[state and ledger contracts](references/state-and-ledger-contracts.md). If a
state JSON exists, run:

```bash
python3 <skill-dir>/scripts/validate_paper_state.py <state.json>
```

Use another available Python 3 launcher when `python3` is unavailable. The
state file records evidence; it does not override current files or governance.

### Inheriting research-pipeline artifacts

When the repository carries `research/STATE.md`, the `$research-pipeline` R
stages own the science and this skill owns the manuscript, running inside R4
and R5. Do not re-derive what an earlier R stage already decided:

- `S1` inherits the R3 ledgers (`paper/ledger/*`, `reports/<run>/RESULT.md`).
  Verify provenance and status values; do not rebuild the ledger from prose.
- `S2` inherits `paper/FRAMING.md` and `paper/STORY_SPINE.md` as thesis, RQs,
  reader value, and narrative order. Locking `S2` additionally requires three
  items: a figure and table plan (`paper/FIGURE_PLAN.md`, one conclusion
  sentence per artifact, Figure 1 decided first), a style contract (the
  `$paper-style-profiler` bundle at `.paper-style/` with `WRITING-CONTRACT.md`
  and `STYLE-STATE.json`, its validator passing and the `STYLE-STATE.json`
  status one of `PROFILE_SAVED`, `TARGET_AUDITED`, or `STYLE_APPLIED`), and a spine
  settlement check (the branch chosen in `paper/STORY_SPINE.md` after R3
  matches the ledger: the evidence its turning point relies on is still
  `VERIFIED_CURRENT`, claim strength does not exceed the ledger, section order
  follows that branch, and the R1 version is archived).
- A mismatch between an inherited artifact and current evidence is a rollback
  to that R stage, recorded in `research/STATE.md` as `回退到 R<n>`, not a
  patch inside `S2`-`S4`. Weakening wording is admissible only when the
  ledger never allowed the stronger claim.

The full R-to-S table is in
`research-pipeline/references/orchestrator-mapping.md`.

## Build the evidence and claim ledgers

Classify every material input as one of:

- `VERIFIED_CURRENT`: current, traceable evidence admissible for the paper.
- `CONTROLLED_OR_RETROSPECTIVE`: usable only with its stated conditions.
- `EXPLORATORY_OR_CANDIDATE`: useful for planning, not for result claims.
- `SUPERSEDED_OR_INVALID`: retained as history, excluded from current claims.
- `MISSING_OR_UNRESOLVED`: unavailable or insufficiently verified.

For each material claim, record its source, population or corpus, protocol,
metric, comparison set, result, permitted wording, and prohibited upgrade.
Preserve `abstain`, unresolved, negative, invalidated, and superseded outcomes.
Never silently screen, relabel, merge, or omit them to improve the narrative.

## Use a bounded question-finding loop

Read [question-finding loop](references/question-finding-loop.md) when the
workflow includes research design, interpretation of an important finding,
Results or Discussion restructuring, anomaly triage, experiment triage,
reviewer stress testing, or deadline convergence. Keep `S0`-`S7` as the outer
stage system; do not add a later-stage label merely because the inner loop
generated another question.

Separate data, directly supported findings, bounded implications, and broader
interpretations. Treat pre-protocol and post-finding literature checks
differently. A technically answerable question does not authorize a new
analysis or experiment: record a safe disposition, obtain user authorization,
and freeze an outcome-independent protocol before execution. A general
principle is optional and must not exceed the evidence or population.

If a machine-readable question-finding ledger exists, run:

```bash
python3 <skill-dir>/scripts/validate_question_finding_ledger.py <ledger.json>
```

The validator checks structure and fail-closed state combinations; it does not
prove scientific importance, truth, or necessity.

## Route work to companion skills

Read [skill routing](references/skill-routing.md) when choosing a companion.
Read [external skill locks](references/external-skill-locks.md) before invoking
the installed figure, diagram, or table engines. Use only skills available in
the current environment.

- Use `$paper-reading` for source-grounded paper reading, comparison, and
  related-work analysis.
- Use `$paper-storytelling` for the story spine, the six-step introduction,
  the Figure 1 judgment, Answer-to-RQ boxes, and the experiment-report symptom
  checklist at `S3` and `S4`.
- Use `$paper-style-profiler` to build, refresh, or audit the repository style
  contract before drafting; the contract is an `S2` input.
- Use `$scientific-visualization` for data-backed publication plots and their
  export, accessibility, metadata, and visual audits.
- Use `$drawio-skill` for editable method, architecture, protocol, and workflow
  diagrams.
- Use `$publication-chart-skill` to lock the evidence contract and decide
  figure versus table and the representation family; its `pubtab` branch then
  owns publication tables, table conversion, and previews. Data plots still go
  to `$scientific-visualization`; `pubfig` output does not replace that
  integrity and export route.
- Use `$academic-humanizer` only after the relevant claims and terminology are
  stable; its role is drafting or minimal prose repair, not scientific truth.
- Use `$paper-review` for graded review (L1 framing and potential gate, L2
  evidence chain, L3 pre-submission) of any target venue; it loads the venue
  profile named in `paper/VENUE_PROFILE.md` (one file per venue under its
  `references/venues/`) and falls back to its generic rubric otherwise.
- For a security venue, still use `$paper-review` with the venue profile from
  `paper/VENUE_PROFILE.md`; when that venue has no profile under its
  `references/venues/`, also read
  [security venue review](references/security-venue-review.md) as a
  supplement. Do not use an economics referee workflow.
- Use `$pdf` when final rendering or PDF layout matters.
- Use `$jupyter-notebook` only when the requested deliverable or reproducibility
  workflow genuinely needs a notebook.
- Use `$Spreadsheets` only when the requested deliverable is a workbook or
  spreadsheet, not merely because the paper contains a table.

If the best companion is unavailable, state the gap and perform only the work
that can be done reliably without pretending that the missing review or
validation occurred.

An external skill's dependency-install default does not override repository or
user authority. For repository-backed papers, do not install packages into the
project interpreter, replace its lockfile, or bootstrap a new TeX distribution
without explicit authorization. Probe first; use an isolated validation
environment when practical; otherwise stop at a specification and report the
missing runtime.

## Draft in evidence-sized units

For an empirical paper, the default order is Methods and Results, then
Discussion and Threats, then Introduction and Related Work, and finally
Abstract, Conclusion, and title. Change this order when the existing manuscript
or user request makes another sequence more coherent.

When `paper/FIGURE_PLAN.md` exists, render the planned figures and tables
before the Results prose that depends on them, and write the prose to the
rendered artifact rather than the reverse; the plan's one-sentence conclusion
becomes the caption opener. Introduction, abstract, and conclusion follow the
`$paper-storytelling` spine: a six-step introduction, an Answer-to-RQ box
after each research question, and a conclusion that restates the story
without repeating the numbers.

Before drafting a unit:

1. Name its rhetorical job and admissible claims.
2. Identify its supporting evidence and locked terminology.
3. Mark missing citations, assumptions, or results instead of filling them.
4. Decide whether the output is an outline, zero draft, revision, or candidate
   final text.

For a Results unit, distinguish the question, protocol, data, finding, and
bounded implication when those layers exist. Use a neutral question heading
when the result is negative, mixed, or unresolved; never make a heading
stronger than its evidence. For Discussion, keep integrated interpretation,
candidate explanations, limitations, and future-study designs visibly
separate.

Read [narrative integrity and rebuttal](references/narrative-integrity-and-rebuttal.md)
when drafting or revising the title, abstract, introduction, or Figure 1; when
wording summarizes a quantity; when partner or restricted evidence is used;
when deadline pressure shapes decisions; or when preparing public materials,
research statements, or job talks.
Route reader-visibility decisions (problem naming, why-now, Figure 1 judgment,
main versus appendix allocation) to `$paper-framing` first.

After drafting, compare source and output for numbers, direction, baseline,
causal strength, uncertainty, scope, citations, and terminology. Keep edits
focused and reviewable. Do not rewrite competent text merely for variation.
Before claiming `S4`, run the `$paper-storytelling` experiment-report symptom
checklist on the draft and confirm that every number in prose traces to the
ledger or an output file.

## Gate figures and tables as evidence

A figure or table is part of the scientific argument, not decoration.

Before producing a manuscript figure/table package, write a visual contract
that gives each artifact and each panel a distinct question, evidence source,
estimator, uncertainty rule, and manuscript role. Read
[figure and table quality gates](references/figure-table-quality-gates.md) when
the package is multi-panel, mixes a figure and a table, highlights a preferred
method, or the user requests iterative visual review.

- Route data plots through `$scientific-visualization`, editable schematics
  through `$drawio-skill`, and publication tables through the table branch of
  `$publication-chart-skill`.
- Tie every displayed value to an authoritative source and explicit
  transformation.
- Do not subtract, merge, or compare values from incompatible pools, protocols,
  populations, or stages.
- Treat captions, notes, labels, axis titles, highlighting, and significance
  marks as claims subject to the same ceiling as prose.
- Require source code or another reproducible construction path for data-backed
  visuals and tables.
- Keep the external engine responsible for rendering and format-specific QA;
  keep this orchestrator responsible for authority, evidence compatibility,
  claim ceilings, venue routing, and manuscript-wide consistency.

When the user explicitly requests strict independent review, freeze the rubric
and artifact hashes before review. Unless the user separately defines a
full-manuscript rubric, these scores apply only to the frozen figure/table
artifact package and must not be reported as scores for the whole manuscript.
Use three or four separately executed reviewers covering visual-design,
statistical-graphics, and venue-production roles. Give each reviewer the same
frozen artifacts, visual contract, and rubric in an isolated pass; do not share
another reviewer's findings or scores until all reviews for that round are
collected. Do not describe multiple role prompts from one uninterrupted
self-review as independent. If separate review execution is unavailable, fail
closed and report that the independence requirement was not met.

Bind every review round to the same rendered figure and table. A strict round
passes only when each reviewer independently clears every requested score
threshold and no hard gate or required change remains. Validate the round
record with:

```bash
python3 <skill-dir>/scripts/validate_visual_review.py \
  <review-record.json> --artifact-root <artifact-root>
```

Do not obtain a pass by changing only the reviewers, weakening the rubric,
averaging away a low score, or asking reviewers to raise scores. Revise the
artifact or report an evidence-bound blocker.

## Separate review from revision

- Review is read-only by default. Findings do not authorize manuscript edits or
  new experiments.
- Distinguish verified defects, reviewer inference, venue-fit judgment, and
  unresolved questions.
- A suggestion to add experiments must state the claim gap, minimal design,
  outcome-independent decision rule, and stop condition. It remains a proposal
  until the user authorizes it.
- Reviewer challenges must be classified before routing: already answered by
  frozen evidence, candidate analysis, candidate new experiment, bounded
  limitation, fatal claim gap, or unresolved reviewer inference. Do not hide a
  fatal claim gap in Limitations.
- For rebuttals and camera-ready work, diagnose verdicts such as
  "incremental" or "limited significance" before proposing experiments,
  promise actions rather than outcomes, keep a promise ledger, and never
  submit results with invalid provenance as preliminary evidence. See
  [narrative integrity and rebuttal](references/narrative-integrity-and-rebuttal.md).
- For current venue scope, format, page limits, anonymity, data statements, AI
  disclosures, or submission fields, check primary official venue sources and
  record the verification date.
- Never present a simulated decision as an acceptance probability.

## Final artifact and readiness gate

At `S6_ARTIFACT_VERIFIED`, verify the editable source, build log, citations and
references, figures and tables, fonts, clipping, page rendering, and artifact
manifest as applicable. Mechanical success proves only the checked condition.

At `S7_SUBMISSION_READY`, separately report:

- scientific blockers;
- manuscript-content blockers;
- format and artifact blockers;
- author-side metadata and disclosure blockers;
- external actions not yet performed.

Do not upload, submit, email, publish, merge, or push unless the user explicitly
requests that external action and the applicable authorization gate passes.

## Response contract

For stage detection or continuation, lead with:

1. `Current stage`
2. `Verified inputs`
3. `Unknown or blocked`
4. `Next admissible action`
5. `Stop rule`

When the question-finding loop was invoked, also report its answerability and
authorization disposition. Do not describe a proposed analysis or experiment
as work in progress.

After changes, report what changed, the evidence used, checks actually run,
remaining unverified items, and the resulting stage. Distinguish local files,
committed branch state, pushed remote state, and main-branch integration when
repository status matters.
