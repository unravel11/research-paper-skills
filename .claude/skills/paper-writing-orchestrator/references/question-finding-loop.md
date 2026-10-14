# Question-Finding Loop

Read this reference when an end-to-end paper workflow includes research design,
interpretation of an important finding, Results or Discussion restructuring,
anomaly triage, experiment triage, reviewer stress testing, or deadline
convergence. Keep the monotonic `S0`-`S7` stages as the outer governance
workflow; this is a bounded inner loop inside `S1`-`S5`, not a replacement stage
system.

## Core boundary

Writing may expose a scientific question, but it does not create evidence for
the answer. A question being technically answerable does not authorize an
analysis or experiment. Before any new run, separately establish:

- evidence admissibility and data access;
- an outcome-independent protocol and decision rule;
- user or author authorization;
- fit with the current paper objective, resource limit, and stop rule.

Do not reopen a frozen no-new-experiment decision merely because a finding can
generate more questions. Record the question and disposition instead.

## Run the bounded loop

For each core question or important finding:

1. **State the question.** Identify whether it is author-defined,
   literature-derived, finding-derived, or a reviewer challenge. Do not invent a
   hypothesis and present it as pre-existing.
2. **Position it in the literature.** A pre-protocol checkpoint may shape
   novelty, competing explanations, and design. A post-finding checkpoint may
   contextualize a result as `CONFIRM`, `CONTRADICT`, `REFINE`, `EXTEND`, or
   `REFRAME`, but it cannot retroactively make an analysis prospective or
   preregistered.
3. **Separate the inference layers.** Record the observed data, the finding
   directly supported by those data, and at most a bounded implication. State
   assumptions, uncertainty, comparison set, and plausible competing
   explanations. Distance labels such as one-hop or two-hop are writing aids,
   not evidence grades.
4. **Triage anomalies.** Classify an unexpected result as a suspected technical
   defect, non-reproducible or unresolved variation, or a reproducible anomaly.
   Never overwrite the old result silently. Preserve its artifacts and status,
   record the diagnosis, and bind any corrected run to a new protocol and
   lineage. Rewriting a research question remains an author-owned proposal.
5. **Interrogate the finding.** Generate only material questions about whether,
   what, how, why, when, where, extent, boundary conditions, or competing
   explanations. A long question list is not progress by itself.
6. **Choose one safe disposition.** Use the controlled dispositions below.
7. **Route the statement.** Place supported observations and bounded
   implications in Results; integrated interpretation in Discussion; an
   important question blocked by a stated study constraint in Limitations; and
   a concrete design for that unresolved question in Future Work. Use
   `DO_NOT_CLAIM` or redesign when the evidence chain fails.

## Answerability dispositions

- `ANSWERABLE_FROM_FROZEN_EVIDENCE`: the answer is already supported by an
  admissible frozen analysis; no new run is implied.
- `PROPOSE_TARGETED_ANALYSIS`: an additional analysis might answer the question.
  Freeze its inputs, estimand, comparison, metric, multiplicity or selection
  handling, decision rule, and stop condition before execution.
- `PROPOSE_NEW_EXPERIMENT`: new data, labels, systems, models, or experimental
  work would be required. Keep it as a proposal until explicitly authorized.
- `OUT_OF_SCOPE_FUTURE_STUDY`: the question matters but exceeds the current
  objective or resource boundary.
- `FATAL_CLAIM_GAP`: the central claim is not supported under the current
  design. Redesign the study or weaken/remove the claim; do not hide it as a
  routine limitation.
- `UNRESOLVED_ABSTAIN`: current evidence cannot support a stable answer or
  actionable proposal.

`PROPOSE_TARGETED_ANALYSIS` and `PROPOSE_NEW_EXPERIMENT` are never execution
authorization. Post-hoc analyses remain labeled exploratory or retrospective
unless a new outcome-independent protocol was frozen before that analysis.

## Results and Discussion rules

- Organize a Results unit around its rhetorical question and supported answer,
  not merely around a familiar technique label. A neutral question title is
  preferable when results are negative, mixed, or unresolved; never turn a
  heading into a stronger claim than the section supports.
- A useful unit may follow `Question -> protocol -> data -> finding -> bounded
  implication`, but omit a step that the evidence cannot support.
- Integrated interpretations must remain compatible with every contributing
  finding and population. Do not merge incompatible pools or protocols to make
  a broader narrative.
- A general principle is optional. When present, label whether it is a bounded
  supported interpretation, a candidate explanation, or an unresolved idea.
  Descriptive, measurement, audit, and negative-result papers are not deficient
  merely because they do not establish a mechanism.
- A meaningful limitation follows `finding -> important unresolved question ->
  study constraint -> affected inference -> checks already performed -> residual
  risk`. Future work should name a design that could answer that question, not a
  generic wish list.

## Reviewer stress test and convergence

For the three most material reviewer challenges, classify each as:

- answerable from already frozen evidence;
- candidate targeted analysis or explanation;
- candidate new experiment;
- out of scope and suitable for a bounded limitation;
- fatal claim gap requiring redesign or claim contraction;
- unresolved or reviewer inference requiring author judgment.

Before continuing the loop, restate the minimum sufficient story and stop rule.
Priority goes to questions that can invalidate the central claim, expose a fatal
design defect, distinguish a material competing explanation, or establish a
necessary boundary. Stop extending Results when the central question is
supported under the frozen claim ceiling, material fatal challenges are closed
or explicitly reflected in claim contraction, and the remaining questions
require work outside the authorized study. This is an author-owned scientific
judgment, not a validator result.

## Optional question-finding ledger

For a short task, use this table:

| Question ID | Origin | Evidence IDs | Data | Finding | Bounded implication | Competing explanations | Anomaly status/lineage | Answerability | Authorization | Protocol | Execution | Claim impact | Manuscript disposition | Stop condition |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

For a long-running workflow, use a machine-readable JSON object with
`schema_version`, `paper_id`, and `questions`. Each question record uses the
same fields in snake case plus `literature_position` and `literature_timing`.
Validate it with:

```bash
python3 <skill-dir>/scripts/validate_question_finding_ledger.py <ledger.json>
```

The validator checks shape and safe state combinations. It does not establish
that a scientific question is important, an interpretation is true, or an
experiment is necessary.
