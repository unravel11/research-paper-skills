# Narrative Integrity, Rebuttal, and Dissemination

Read this reference when drafting or revising the title, abstract,
introduction, or Figure 1; when wording must summarize a quantitative result;
when responding to reviewers or preparing a camera-ready version; when partner
or restricted evidence enters the paper; when deadline pressure is shaping
decisions; or when preparing a thread, project page, press text, talk, or video
for an accepted or posted paper.

Framing work that decides what the reader should see — diagnosis of an
"incremental" verdict, why-now, problem naming, Figure 1 judgment, main versus
appendix allocation — belongs to `$paper-framing` and its
`reader-visibility.md`. This reference keeps those decisions inside the claim
ceiling once text, figures, responses, and public materials are produced.

## 1. Visibility edits are semantic edits

Retitling, renaming the problem, swapping Figure 1, or rewriting the abstract
opening can change what a reader believes even when no number changes. Treat
these as claim-bearing revisions:

- Record them in the revision ledger with the intended semantic change, not as
  `no intended semantic change`.
- Re-run the S4 strength-consistency check across title, abstract, Figure 1,
  introduction, results, and conclusion.
- A renamed construct (for example "patterns" becoming "concepts" or
  "knowledge") must map to a measured construct in the claim ledger. If it does
  not, keep the narrower term.
- A method name or acronym may be memorable but must not overstate scope
  (`heuristic` versus `framework`) or hide a component that changes cost or
  complexity.

## 2. Calibrate adjectives to numbers

Every evaluative adjective tied to a quantity cites the number and comparison
it summarizes. Record it in the claim ledger's `Allowed strength` column, for
example `modest overhead (+8.7% wall-clock vs. baseline, same hardware)`.

- Do not invent universal thresholds such as "under 10% is negligible". Use the
  venue's or field's documented convention when one exists; otherwise prefer
  the number itself.
- `significant` requires a reported test or interval; `consistent` requires
  that all reported settings agree, or a stated count such as "2 of 3".
- The same calibrated wording binds the paper, rebuttal, slides, and public
  materials.

## 3. Main text versus appendix

`$paper-framing` (`reader-visibility.md`, section 7) owns the four conditions
that separate organizing evidence from selecting it. At drafting time, verify
that the selection rule appears in the text or caption and that abstract and
conclusion strength reflect the full result set.

A limitation that conditions the central claim stays in the main text. A
collaborator's or partner's preference to shorten limitations does not move a
condition on the headline claim into an appendix.

## 4. Deadline-pressure gates

These gates do not relax because of a deadline, an internship, a job market,
or a compute allocation:

- **Invalid provenance.** A result produced with leakage, such as validation
  data used for hyperparameter selection and also for reporting, has status
  `SUPERSEDED_OR_INVALID`. Either remove it or rerun it under a valid protocol.
  Do not submit its numbers or trend as preliminary evidence.
- **Preliminary claims.** "Preliminary results show consistent trends" is
  admissible only when the producing run is protocol-valid and merely
  incomplete in scale or seeds. Record what was run, the count, and what
  remains.
- **Outcome-dependent promises.** Do not promise a result that has not been
  observed ("full results will confirm"). Promise the analysis and its
  reporting, not its outcome.
- **Lucky outcomes.** A rerun that happens to match an earlier placeholder does
  not validate the earlier process. Record the lineage honestly in the
  revision ledger.

## 5. Restricted, partner, or non-reproducible evidence

- Evidence the authors cannot inspect or recompute — partner-internal
  evaluation, restricted data, withheld logs — is recorded with that
  provenance. Use `CONTROLLED_OR_RETROSPECTIVE` with the restriction stated, or
  `MISSING_OR_UNRESOLVED` when its validity cannot be assessed.
- Claims resting on it carry the qualifier in the claim itself, for example
  "in the partner's internal evaluation". Do not leave the qualifier only in
  Limitations.
- An email or sign-off stating that results were "confirmed" is a provenance
  note, not validation. Record which checks the authors themselves performed.
- An algorithm simplified for integration ("update weights every k steps"
  instead of an online estimator) is a different method variant. Name it
  separately; do not transfer claims across variants without evidence.
- Citing another group's large-scale result supports plausibility, not your
  method's scalability. Label it as discussion and context, never as evidence.

## 6. Reviewer responses and meta-reviews

### Diagnose before responding

For verdicts such as "technically sound but limited significance",
"incremental", or "unclear difference from concurrent work", route the
diagnosis to `$paper-framing` (`reader-visibility.md`) before planning
experiments. Classify each material point with the S5 categories and, in
addition, tag whether it is primarily a visibility, difference, evidence, or
venue-fit issue. Several comments may share one root cause.

### Admissible response forms

| Form | Use when | Constraint |
|---|---|---|
| Answer from frozen evidence | The paper or appendix already answers it | Point to the exact location; do not restate it more strongly |
| Targeted analysis completed | A new analysis ran under an outcome-independent protocol | Report it with its protocol and add it to the evidence ledger |
| Scoped discussion | The question exceeds available resources | Label it as discussion; cite context as context; state what remains unknown |
| Commitment | A change will be made in the final version | Commit to actions and reporting, not to outcomes; record it in the promise ledger |
| Concede and contract | The point exposes a real gap | Narrow the claim in the paper as well as in the response |

Do not answer a fatal claim gap with a commitment or a discussion paragraph.

### Promise ledger

Track every rebuttal commitment until camera-ready:

| Promise ID | Reviewer point | Exact promised action | Evidence status at rebuttal | Camera-ready location | Delivered? | Claim impact if result differs |
|---|---|---|---|---|---|---|

Camera-ready reopens S4 for the affected claims. If a promised result differs
from the rebuttal's description, report the difference in the final paper; do
not silently align the wording.

## 7. Public materials and credit

Threads, project pages, press releases, talks, videos, and job materials derive
from the paper and inherit its claim ceiling.

- Before release, map each public sentence to a claim-ledger row. Reject any
  sentence that has no row or that exceeds the row's allowed strength, for
  example "we discovered that data matters" when the contribution is a specific
  method under specific assumptions.
- A teaser figure that looks like data must be data. A conceptual
  illustration must be labeled as conceptual and must not show smoother or
  larger effects than observed.
- A schematic may compress steps but must not omit a component that changes
  cost, complexity, or reproducibility.
- When a communications office or collaborator rewrites the text, review the
  final version against the ledger. Origin stories and attributions are the
  authors' to state accurately; flag any mismatch for the authors and do not
  resolve it yourself.
- Research statements, grant text, and job talks separate agenda sentences
  (questions or future tense, may exceed current evidence) from result
  sentences (bound by each paper's claim ceiling). Follow each agenda sentence
  with the part of it existing work actually covers. A bolder vision widens the
  agenda, not the strength of results. Distinguish one's own line from a
  collaborator's by the questions answered, not by new terminology. See
  `$paper-framing` (`reader-visibility.md`, section 10).
- Leading with a failure or boundary figure is legitimate when that is the most
  important result.
- Author order, equal-contribution marks, and contribution statements are
  author-owned decisions under the venue's and institution's policies. Flag
  contribution statements that do not match recorded roles; do not decide
  them.
