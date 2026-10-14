# Stage Playbook

Read this reference when starting, detecting, or advancing an end-to-end paper
workflow. A stage is a claim about verified state, not a label chosen for
convenience.

When the project carries `research/STATE.md`, the `$research-pipeline` R stages
own the science and this playbook runs inside R4 and R5: `S1` inherits the R3
ledgers, `S2` inherits `paper/FRAMING.md` and `paper/STORY_SPINE.md`, and a
mismatch with current evidence is a rollback to that R stage rather than a
patch here. See `research-pipeline/references/orchestrator-mapping.md`.

## S0 Authority resolved

If the following evidence has not been established, report `PRE_S0` and name
`S0` as the earliest unmet gate. `PRE_S0` is a diagnostic response label, not a
persisted stage value.

Required evidence:

- editable manuscript source or new-paper workspace;
- target paper line or authoritative version;
- applicable repository instructions;
- branch, HEAD, and worktree status for repository-backed work;
- target venue or an explicit `UNDECIDED` value.

Stop when two manuscript versions compete, the requested file is generated or
archived, or authority cannot be established.

## S1 Evidence locked

Required evidence:

- evidence inventory with provenance status;
- claim ledger with permitted wording and ceiling;
- explicit separation of current, controlled, candidate, invalid, and missing
  material;
- known protocol, population or corpus, metric, comparison set, and exclusions;
- declared experiment decision: no new experiment, analysis only, proposed
  targeted work, redesign, or unresolved.

For research-design or finding-interpretation work, also require:

- a question-to-evidence record that separates data, directly supported
  finding, bounded implication, and competing explanations as applicable;
- literature checkpoint timing recorded as pre-protocol or post-finding
  contextualization; post-finding reading cannot retroactively make a protocol
  prospective;
- every new analysis or experiment recorded only as a disposition until user
  authorization and an outcome-independent protocol freeze exist;
- anomalies retained with lineage as suspected defect, non-reproducible or
  unresolved variation, or reproducible anomaly rather than silently removed.

This gate does not require that every desirable experiment exists. It requires
honesty about what exists and what it can support.

## S2 Argument locked

Required evidence:

- one-sentence paper thesis;
- research questions;
- contribution list mapped to evidence;
- section outline with rhetorical jobs;
- figure and table plan (`paper/FIGURE_PLAN.md` when research-pipeline is in
  use), including the distinct question and manuscript role of each planned
  artifact or panel, one conclusion sentence per artifact, and Figure 1
  decided first;
- a style contract from `$paper-style-profiler` whose bundle validator passes;
- a spine settlement check against the ledger: the branch chosen in
  `paper/STORY_SPINE.md` after R3 is the one the evidence supports, the
  evidence its turning point relies on is still `VERIFIED_CURRENT`, claim
  strength does not exceed the ledger, the section order follows that branch,
  and the R1 version is archived;
- related-work positioning plan;
- explicit non-claims and external-validity boundary.
- reader-visibility decisions from `$paper-framing` when applicable: problem
  name mapped to a measured construct, why-now basis or an explicit absence,
  the judgment Figure 1 must show, and the main versus appendix selection rule;
- a minimum sufficient story and stop rule under the current objective;
- a question-to-section and question-to-evidence map, including explicit
  dispositions for material unresolved questions.

The outline may change later, but changes to the thesis, RQs, or contribution
ceiling reopen this gate.

## S3 Section drafted

Required evidence for each completed unit:

- named source bundle;
- draft status: outline, zero draft, revised candidate, or author-approved text;
- completed source-to-text comparison;
- missing evidence and unresolved terminology kept visible outside clean prose;
- no invented citation, number, method detail, result, or author decision.
- Results units do not conflate data, finding, and interpretation, and headings
  do not exceed the supported answer;
- anomaly and negative-result dispositions remain visible rather than being
  rewritten into the expected hypothesis.
- when a figure plan exists, the figures and tables the unit cites are
  rendered before its prose, and the plan's conclusion sentence opens the
  caption.

Several sections may be drafted in one task when the evidence is stable and the
user requests it. Do not call the whole manuscript complete merely because text
exists for every heading.

## S4 Manuscript integrity checked

Required checks:

- title, abstract, introduction, results, discussion, and conclusion describe
  the same findings at the same strength;
- all repeated numbers and comparison directions agree with authoritative
  results;
- terminology, RQ labels, dataset names, stage names, and metric definitions are
  consistent;
- figures, tables, captions, and prose agree;
- figure and table roles are non-redundant, or any deliberate duplication has
  an explicit lookup, accessibility, or cross-reference purpose;
- citations exist and the cited source supports the attached claim, or the item
  is explicitly unresolved;
- limitations and threat-model assumptions are not erased by polishing;
- evaluative adjectives cite the number and comparison they summarize, and
  limitations that condition the central claim remain in the main text;
- Figure 1, teaser, and schematic artifacts neither imply unobserved effects
  nor omit components that change cost or complexity;
- deprecated or invalid results have not re-entered the current chain.
- the `$paper-storytelling` symptom checklist is clear: no background opener,
  a real motivating example, Figure 1 within the first two pages, at most two
  numbers per sentence, no internal code names, an answer box after each RQ,
  and a conclusion that does not repeat the numbers;
- every number in prose traces to the ledger or an output file.
- broader interpretations remain compatible with their contributing findings,
  assumptions, populations, and protocols;
- any general principle is optional and labeled at its actual evidence strength
  rather than treated as a maturity requirement;
- each material limitation identifies an important unresolved question, the
  study constraint, affected inference, checks performed, and residual risk;
  future work names a design for that question instead of a wish list.

An automated scan can support this gate but cannot establish it alone.

## S5 Venue reviewed

Use `$paper-review` at the level appropriate to the current manuscript state;
it loads the venue profile (one file per venue under its
`references/venues/`) and falls back to its generic rubric for an unprofiled
venue. For a security venue without a profile, also read
`security-venue-review.md`. At L3, render the PDF and inspect layout, figures,
tables, and font sizes; reading the source alone is not a review.

Required outputs:

- contribution and venue-fit judgment;
- claim-evidence findings;
- scientific and reproducibility risks;
- experiment decision or explicit abstention;
- reviewer-style questions;
- current official format or submission requirements when requested;
- a stop rule for the next revision round.

Classify the three most material reviewer challenges as frozen-evidence answer,
candidate targeted analysis, candidate new experiment, bounded limitation,
fatal claim gap, or unresolved reviewer inference. This classification does
not authorize a run. A fatal claim gap reopens the earliest affected gate or
requires claim contraction; it is not converted into a routine limitation.

For a meta-review or verdict such as "incremental" or "limited
significance", also tag each material challenge as a visibility, difference,
evidence, or venue-fit issue before proposing any experiment.

Review output is advisory. It is not acceptance, probability of acceptance, or
permission to mutate the manuscript.

## S6 Artifact verified

Required evidence as applicable:

- authoritative editable source builds successfully;
- no unresolved citations, references, or fatal compile errors;
- figures and tables are present, legible, and linked to sources;
- figures and tables have been rendered at final manuscript width inside the
  authoritative venue template rather than only as standalone previews;
- every page has been visually inspected after the latest meaningful change;
- fonts, clipping, overlap, page count, anonymity, and metadata have been
  checked;
- a manifest, hash, or other reproducible snapshot is recorded when required.

State exactly what each mechanical check proves and does not prove.

## S7 Submission ready

Required evidence:

- no unresolved scientific blocker under the chosen claim ceiling;
- required manuscript and supplementary files exist;
- current venue requirements have been checked against official sources;
- author names/order, affiliations, corresponding author, funding, conflicts,
  contribution statements, disclosures, data statements, biographies, and
  artifact links are resolved when the venue requires them;
- all remaining external actions are listed.

Submission readiness does not mean submitted. A submission action requires an
explicit user request and separate external confirmation.

## Post-review cycles

Rebuttal, revision, and camera-ready work happen after the external
`SUBMITTED` state. Open the earliest gate the response affects, use the
response forms and promise ledger in `narrative-integrity-and-rebuttal.md`,
and re-run S4 for every claim touched by a promise before the final version.
An accepted paper's public materials inherit the same claim ceiling.

## Reopening a gate

Reopen the earliest affected gate when any of these changes:

- authoritative manuscript version;
- evidence source, protocol, population, pool, or label definition;
- main RQ, thesis, contribution, or claim ceiling;
- figure or table source data;
- target venue or official submission rules;
- final source after artifact verification.
- a new question is accepted as a central RQ or changes the minimum sufficient
  story;
- an anomaly invalidates current evidence, or a new analysis/experiment changes
  the protocol or comparison set.

Do not preserve a later-stage label across a material upstream change.

A target-venue change reopens `S2` for reader framing, takeaway emphasis, and
related-work positioning only. It never changes the main comparison, the
decision rule, or the claim ceiling; a venue's influence on the experiments
enters only through the evidence standard recorded in the R2 protocol.
