# State and Ledger Contracts

Use these contracts for a long-running paper or when the user asks for durable
workflow state. They are optional for a focused one-turn revision.

## Paper brief

```markdown
# Paper Brief

- Paper ID:
- Target venue:
- Editable manuscript authority:
- One-sentence thesis:
- Research questions:
- Contributions:
- Explicit non-claims:
- Evidence freeze or snapshot:
- Current experiment decision:
- Literature checkpoints and timing:
- Minimum sufficient story:
- Stop rule:
- Author-owned unresolved decisions:
```

## Evidence ledger

| Evidence ID | Source | Status | Protocol/population | What it supports | What it cannot support | Validation | Run ID | Output file |
|---|---|---|---|---|---|---|---|---|

`Run ID` names the `reports/<run>/` directory the evidence came from; `Output
file` is the file under `reports/<run>/outputs/` that every number quoted in
prose traces back to. The CSV in `paper/ledger/evidence_inventory.csv` carries
the same columns in snake case. Allowed status values are `VERIFIED_CURRENT`, `CONTROLLED_OR_RETROSPECTIVE`,
`EXPLORATORY_OR_CANDIDATE`, `SUPERSEDED_OR_INVALID`, and
`MISSING_OR_UNRESOLVED`.

## Claim ledger

| Claim ID | Manuscript location | Exact claim | Evidence IDs | Allowed strength | Prohibited upgrade | Status |
|---|---|---|---|---|---|---|

Use `SUPPORTED`, `WEAKEN`, `ABSTAIN`, or `REMOVE_FROM_CURRENT_CHAIN` for claim
status. A claim may cite several evidence IDs only when their protocols and
comparison sets permit combination.

## Optional question-finding ledger

Use this ledger when the workflow includes research design, important finding
interpretation, anomaly triage, Results or Discussion restructuring, reviewer
stress testing, or experiment triage.

| Question ID | Origin | Evidence IDs | Data | Finding | Bounded implication | Competing explanations | Literature position/timing | Anomaly status/lineage | Answerability | Authorization | Protocol | Execution | Claim impact | Manuscript disposition | Stop condition |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Allowed answerability values are
`ANSWERABLE_FROM_FROZEN_EVIDENCE`, `PROPOSE_TARGETED_ANALYSIS`,
`PROPOSE_NEW_EXPERIMENT`, `OUT_OF_SCOPE_FUTURE_STUDY`, `FATAL_CLAIM_GAP`, and
`UNRESOLVED_ABSTAIN`. Answerability does not imply authorization. Preserve
pre-protocol and post-finding literature timing, and never use a post-hoc
contextualization to claim prospective design.

For long-running work, store the ledger as JSON and run:

```bash
python3 <skill-dir>/scripts/validate_question_finding_ledger.py <ledger.json>
```

The JSON object carries `schema_version` (the string `"1"`), `paper_id`, and a
non-empty `questions` list. Each question record has exactly these fields; the
validator rejects an unknown enum value and a missing nullable field:

| Field | Type | Allowed values | Meaning |
|---|---|---|---|
| `question_id` | string | non-empty, unique | row key |
| `question` | string | non-empty | the question as stated |
| `origin` | enum | `AUTHOR_DEFINED`, `LITERATURE_DERIVED`, `FINDING_DERIVED`, `REVIEWER_CHALLENGE` | where the question came from |
| `evidence_ids` | list of strings | evidence ledger IDs | admissible evidence the answer rests on |
| `data_statement` | string or null | free text | the observed data (the `Data` column) |
| `finding` | string or null | free text | the finding those data directly support |
| `bounded_implication` | string or null | free text | at most one bounded implication |
| `competing_explanations` | list of strings | free text | plausible alternative explanations |
| `literature_position` | enum | `CONFIRM`, `CONTRADICT`, `REFINE`, `EXTEND`, `REFRAME`, `UNRESOLVED` | how the literature positions the finding; any value but `UNRESOLVED` needs a checked timing |
| `literature_timing` | enum | `PRE_PROTOCOL`, `POST_FINDING_CONTEXT`, `BOTH`, `NOT_CHECKED` | when the literature checkpoint happened |
| `anomaly_status` | enum | `NOT_ANOMALOUS`, `SUSPECTED_TECHNICAL_DEFECT`, `NONREPRODUCIBLE_OR_UNRESOLVED`, `REPRODUCIBLE_ANOMALY` | anomaly triage class |
| `lineage_note` | string or null | free text; required when anomalous | lineage of the old and any corrected run |
| `answerability_disposition` | enum | the six answerability values above | the one safe disposition chosen |
| `authorization_status` | enum | `NOT_REQUIRED_EXISTING_EVIDENCE`, `NOT_REQUESTED`, `PROPOSED`, `AUTHORIZED`, `REJECTED`, `NOT_APPLICABLE` | user authorization for proposed work |
| `protocol_status` | enum | `FROZEN`, `PROPOSED_NOT_FROZEN`, `NOT_APPLICABLE`, `UNRESOLVED` | outcome-independent protocol state |
| `execution_status` | enum | `NOT_APPLICABLE`, `NOT_STARTED`, `IN_PROGRESS`, `COMPLETED`, `FAILED`, `INVALIDATED` | state of the authorized work |
| `claim_impact` | enum | `NO_CHANGE`, `SUPPORT_IF_VALIDATED`, `WEAKEN`, `REMOVE`, `REOPEN_S1`, `REOPEN_S2`, `UNRESOLVED` | effect on the claim ledger |
| `manuscript_disposition` | enum | `RESULTS`, `DISCUSSION`, `LIMITATION`, `FUTURE_STUDY`, `DO_NOT_CLAIM`, `REDESIGN_REQUIRED`, `PENDING` | where the statement is routed |
| `stop_condition` | string or null | free text; required for a proposal | when the proposed work stops |

In `Allowed strength`, an evaluative adjective that summarizes a quantity
cites that quantity and its comparison, for example `modest overhead (+8.7%
wall-clock vs. baseline)`. Evidence the authors cannot inspect or recompute
states that restriction in the evidence row and in the claim wording.

## Revision ledger

| Revision ID | Trigger | Files/spans | Intended semantic change | Evidence used | Checks | Remaining risk |
|---|---|---|---|---|---|---|

Language-only edits should state `no intended semantic change`. Retitling,
renaming the problem or method, replacing Figure 1, or rewriting the abstract
opening are semantic edits even when no number changes. If the actual
change alters a claim, reopen the appropriate upstream gate.

## Optional machine-readable state

```json
{
  "schema_version": "1",
  "paper_id": "paper-id",
  "target_venue": {
    "name": "TSE",
    "family": "se",
    "requirements_checked_on": null
  },
  "authority": {
    "kind": "repository",
    "workspace": "<workspace>",
    "branch": "<branch-or-null>",
    "head": "<commit-or-null>",
    "status": "unknown",
    "manuscript": "<editable-source>"
  },
  "stage": "S1_EVIDENCE_LOCKED",
  "gates": {
    "authority_resolved": true,
    "evidence_locked": true,
    "argument_locked": false,
    "draft_present": false,
    "integrity_checked": false,
    "venue_reviewed": false,
    "artifact_verified": false,
    "submission_blockers_resolved": false
  },
  "artifacts": {
    "evidence_ledger": "<path-or-null>",
    "claim_ledger": "<path-or-null>",
    "question_finding_ledger": "<path-or-null>",
    "paper_plan": null,
    "manuscript": "<editable-source>",
    "integrity_report": null,
    "venue_review": null,
    "final_pdf": null,
    "artifact_validation": null,
    "submission_readiness": null
  },
  "claim_ceiling": ["<bounded claim>"],
  "open_blockers": ["<unresolved item>"],
  "last_verified_at": "<ISO-8601 timestamp or null>"
}
```

Run `scripts/validate_paper_state.py` after editing this JSON. Validation checks
shape and stage consistency; it does not verify that the referenced science is
true or that paths refer to current artifacts. From the stage named below
onward, the validator requires these `artifacts.*` keys to be non-empty
strings (earlier stages may leave them null): `S1` `evidence_ledger` and
`claim_ledger`; `S2` `paper_plan`; `S3` `manuscript`; `S4` `integrity_report`;
`S5` `venue_review`; `S6` `final_pdf` and `artifact_validation`; `S7`
`submission_readiness`. `question_finding_ledger` is optional at every stage
and may stay null.

## Rebuttal promise ledger

| Promise ID | Reviewer point | Exact promised action | Evidence status at rebuttal | Camera-ready location | Delivered? | Claim impact if result differs |
|---|---|---|---|---|---|---|

Promise actions and reporting, not outcomes. Close every row before
camera-ready; a differing result is reported, not aligned to the rebuttal.

## Submission blocker ledger

| Class | Item | Required by | Evidence/status | Owner | Blocks submission? |
|---|---|---|---|---|---|

Keep scientific, manuscript, format, artifact, author-metadata, and external-
action blockers in separate rows.
