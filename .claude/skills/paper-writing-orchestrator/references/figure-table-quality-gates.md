# Figure And Table Quality Gates

Read this reference when an active manuscript workflow needs a multi-panel
figure, a figure-plus-table package, evidence-bearing highlighting, or an
explicit iterative visual-review loop. External skills own rendering;
`paper-writing-orchestrator` owns the evidence contract, artifact roles,
manuscript integration, and review gate.

## 1. Lock the visual contract before rendering

Record one contract for the package:

- intended manuscript claim and research question;
- authoritative source data and transformation path;
- unit of analysis and unit of replication;
- field names, units, metric direction, and eligible comparison set;
- estimator, uncertainty interval, dependence handling, and `n`;
- missing, censored, excluded, and failure-event handling;
- target venue template, intended physical width, and submission phase;
- the distinct job of the figure and table.

For every panel, complete this sentence:

> This panel answers ___ using ___ that the other panels do not already show.

Delete or redesign a panel when the sentence cannot be completed with a real
information difference. Different geometry or color is not a distinct role.

The normal paired-deliverable split is:

- figure: rapid perception of pattern, distribution, uncertainty, relationship,
  or diagnostic behavior;
- table: exact values, definitions, and reproducible lookup.

Deliberate duplication is allowed only for a stated accessibility, lookup,
cross-reference, or venue requirement.

## 2. Representation and statistical gates

- Prefer position on a common scale. For categorical estimates, a compact
  point-interval or forest-style display is normally stronger than bars.
- Show raw observations when feasible and when their unit is not misleading.
- Every displayed aggregate axis needs an uncertainty policy. A two-dimensional
  mean comparison normally needs uncertainty on both axes or a captioned reason
  that one axis is descriptive only.
- State the dependence assumption used by every interval. Independent-run
  intervals require an explicit independence assumption; shared-task,
  shared-seed, clustered, or repeated-measure designs require a dependence-aware
  interval or an explicit decision not to show inferential uncertainty.
- When the same replicate produces multiple metrics, retain its pairing in the
  source and display it when useful. Do not calculate paired differences until
  the design confirms the pairing.
- Use `trade-off` only when observed alternatives conflict across objectives.
  Otherwise use `comparison`, `performance-runtime plane`, or `dominance` as
  supported by the evidence.
- Axis and column wording must trace to a source field and unit. Plotting code
  may shorten a label but may not strengthen its semantics.
- Do not infer significance, superiority, or a winner from point estimates or
  non-overlapping intervals alone.

## 3. Visual hierarchy and accessibility gates

- Design and inspect at the final physical width. Body text and tick labels
  should normally remain at least 7 pt unless the live venue instructions say
  otherwise.
- Use one restrained typography hierarchy. Panel labels should orient rather
  than dominate.
- Prefer neutral comparison marks plus at most one predeclared accent when a
  focal role is scientifically or rhetorically legitimate.
- Do not hardcode visual emphasis from a method name such as `Proposed`.
- Bind any accent, bolding, or annotation to a visual contract that states the
  eligible set, primary metric, metric direction, tie rule, and meaning of the
  emphasis. Emphasis does not imply significance unless a reported analysis
  supports that claim.
- Color must have a non-color cue. Avoid colored method text as the only key;
  use position, shape, line style, direct black labels, or a compact legend.
- Remove repeated in-panel prose that belongs in the caption. Shorten labels
  before reducing font size.
- Inspect whitespace, label collisions, clipping, grayscale, and downscaled
  readability in the rendered manuscript page.

### Figure 1, teaser, and schematic gates

- A figure that looks like data must be data. State the selection rule for
  representative examples in the caption (random, median by a named metric,
  or author-selected).
- A conceptual illustration is labeled as conceptual and does not depict
  smoother, larger, or more uniform effects than observed.
- A method schematic may compress steps but must not omit a component that
  changes cost, complexity, or reproducibility.
- Text, dividers, and emphasis on Figure 1 are claims under the same ceiling as
  the abstract.

## 4. Publication-table gates

- Default to editable black-on-white `booktabs` styling without vertical rules.
  Use fills or full-row emphasis only when they encode a declared meaning and
  remain legible in grayscale.
- Use decimal-aligned numeric columns such as `siunitx` `S` columns when values
  are compared vertically.
- Report compatible estimates consistently. If score has a mean and interval,
  explain why another continuous aggregate has no interval or report one there
  too.
- State aggregation for counts, failures, and denominators. A bare total is not
  self-defining.
- Keep precision consistent with the source and estimator; do not imply extra
  precision during formatting.
- Prefer a single-column float when the natural table width fits. Use a
  double-column float because the content needs it, not to create empty space.
- Keep table-specific length changes local. Do not emit unused packages or
  global style changes that leak into later floats.
- Compile the final caption, label, notes, and float in the authoritative venue
  template. A standalone table-body preview is an intermediate check only.

## 5. Caption completeness

The caption or adjacent table note should identify, when applicable:

- variables and units;
- estimator and interval type/level;
- `n` and unit of replication;
- dependence or pairing;
- missing/exclusion/failure aggregation;
- metric direction and the exact meaning of emphasis;
- panel roles and any deliberate difference in uncertainty treatment.

Keep the caption self-contained without copying the Results prose.

## 6. Strict independent-review mode

Use this mode only when the user requests a scored iterative review or the
manuscript workflow explicitly adopts it. Ordinary figure/table work still uses
the external skills' normal QA without mandatory multi-agent scoring.

Before the first review:

1. Freeze a rubric and a threshold. Do not lower either after seeing scores.
2. Export the exact artifacts and compute their hashes.
3. Assign at least these three independent roles:
   - visual design and information hierarchy;
   - statistical graphics and evidence integrity;
   - target-venue production and manuscript integration.
4. Give every role the same artifact versions and visual contract. Do not give
   one reviewer another reviewer's score or findings before it submits.
5. Run reviewers in separated agent, process, or context passes. Multiple role
   prompts inside one uninterrupted self-review do not establish independence.
   If separated execution is unavailable, record the round as `FAIL` or
   `UNAVAILABLE`; do not substitute an independence claim.
6. Unless a separate manuscript-wide rubric is frozen, all numeric scores in
   this mode refer only to the figure/table artifact package. Do not reuse them
   as scores for the manuscript, scientific contribution, submission
   readiness, or acceptance.

Each reviewer must score `figure`, `table`, and `overall` on 0--10. A score of
9 means publication-mature for the stated evidence and venue, with no material
design correction remaining. The following are hard gates and cap the affected
artifact below 9:

- untraceable values or incompatible evidence;
- redundant panel without an explicit role;
- undefined or inconsistent uncertainty;
- unsupported semantic label or visual emphasis;
- unreadable final-size text, clipping, or overlap;
- non-editable table when editable text is required;
- missing actual-template integration when the venue is known;
- unresolved required change from that reviewer.

A round passes only if every reviewer independently gives all three scores at
or above the frozen threshold, reports no hard-gate failure, and requests no
remaining change. Do not average scores. If a round fails:

1. merge overlapping findings by root cause;
2. change the smallest owning rule or artifact;
3. regenerate and revalidate all affected formats;
4. start a new review round bound to the new hashes.

Keep reviewer roles and rubric stable across rounds. A new reviewer may replace
an unavailable reviewer, but replacement alone cannot cure a failed artifact.
The validator checks record structure, thresholds, and hashes; it cannot prove
that reviewer executions were genuinely separated, or establish scientific
validity, submission readiness, or venue acceptance.

## 7. Mechanical validation before a passing review

- source-data to summary to figure/table numerical consistency;
- vector output and raster preview;
- final dimensions, raster effective DPI, fonts, and transparency;
- palette/background contrast plus grayscale inspection;
- LaTeX build log, overfull/underfull output, and unused/global dependencies;
- render every affected PDF page and inspect at 100% scale;
- bind the review record to the exported artifact hashes.

Mechanical success proves only those checks. A high simulated-review score is
not an acceptance prediction.
