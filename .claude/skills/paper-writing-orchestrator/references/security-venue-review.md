# Security Venue Review

Use this reference for software and systems security papers when no more
specific installed venue-review skill owns the target. The review is read-only
by default and is evidence bounded.

## Freeze the review snapshot

Record the manuscript source, branch or version, HEAD and worktree status when
repository-backed, evidence bundle, artifact version, target venue, and review
date. Current venue scope and submission rules must come from primary official
sources and include the verification date.

## Review dimensions

### Problem and security relevance

- What protected asset, trust boundary, attacker capability, or policy property
  is in scope?
- Is the security consequence demonstrated, modeled, or only hypothesized?
- Does the problem matter beyond one configuration or implementation accident?

### Threat model and assumptions

- Are attacker knowledge, access, privileges, timing, and goals explicit?
- Are trusted components and excluded attacks explicit?
- Do the evaluation and claims stay inside the threat model?
- Are configuration-conditioned, source-only, controlled, retrospective, and
  runtime findings kept distinct?

### Method and mechanism

- Is the analyzed object defined precisely?
- Does the implementation operationalize the paper's formal definition?
- Are detection, ranking, matching, exploitation, mitigation, and policy truth
  distinguished?
- Are failure, abstention, unsupported inputs, and ambiguous cases represented?

### Evaluation validity

- Do datasets, labels, splits, candidate pools, baselines, metrics, and sampling
  match the stated research question?
- Are training, development, retrospective reconstruction, and untouched
  confirmation separated?
- Are same-pool comparisons kept separate from end-to-end or cross-pool claims?
- Are uncertainty, variance, failure cases, negative results, and sensitivity
  visible?
- Does each experiment test a named claim without upgrading correlation to
  causation or controlled evidence to real-world prevalence?

### Vulnerability and disclosure claims

- Source candidates are not vulnerabilities without the required runtime or
  affected-product evidence.
- A proof of concept is not automatically safe, general, or exploitable in all
  deployments.
- Public, vendor, and CVE status must be independently verified and dated.
- Sensitive exploit detail, affected-party information, and disclosure status
  must respect the user's authorization and responsible-disclosure boundaries.

### Artifacts and reproducibility

- Are source, data, environment, commands, hashes, manifests, and expected
  outputs sufficient for the claimed replay level?
- Are restricted inputs, licenses, redistribution limits, provider aliases, and
  unavailable services explicit?
- Does the artifact prove only mechanical replay, or does it also include an
  independent scientific oracle? Keep these distinct.

### Ethics and risk

- Are participant, telemetry, privacy, dual-use, disclosure, and institutional
  requirements addressed where applicable?
- Are data minimization and access boundaries clear?
- Does artifact release avoid increasing harm beyond the documented benefit and
  authorization?

### Contribution and venue fit

- Is the contribution a new security problem, mechanism, dataset, measurement,
  empirical finding, formalization, artifact, or evaluation discipline?
- What is the closest work, and what exact difference is supported?
- Is novelty carried by evidence and mechanism rather than labels or rhetoric?
- Separate venue fit from scientific validity and both from acceptance.

## Required output

Lead with:

1. `Review snapshot`
2. `Verified contribution and claim ceiling`
3. `Major scientific findings`
4. `Threat-model and evaluation findings`
5. `Artifact, ethics, and disclosure findings`
6. `Venue-fit judgment`
7. `Experiment decision`: no more core experiments, analysis only, targeted
   experiments proposed, major redesign, or abstain for missing inputs
8. `Author questions`
9. `Next stop rule`

Do not report an acceptance probability. Do not execute suggested experiments
or modify the manuscript without a separate user request.

