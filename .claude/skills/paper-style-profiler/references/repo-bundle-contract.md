# Repository Bundle Contract

Default bundle directory: `.paper-style/`. A repository may configure another relative directory. State the location before first write and obey repository authority rules.

Never copy PDFs or extracted full text into this bundle. All stored source paths are repository-relative.

## Complete artifacts

### `STYLE-STATE.json`

Required top-level fields:

- `schema`: `paper_style_state_v1`
- `skill`: `paper-style-profiler`
- `status`
- `generated_at`: UTC ISO-8601 string
- `repository`: object whose `root` must be exactly `"."` (the validator rejects any other value); also record authority label, branch, HEAD, target venue, and research genre when known
- `target`: object with `paths` (a list of unique repository-relative manuscript paths) and `hashes` (a dict mapping each of those paths to its lowercase SHA-256); the validator requires the two key sets to be identical
- `anchors`: three to five objects for a complete profile
- `artifacts`: relative bundle filenames
- `refresh_conditions`: recorded stale checks

Each anchor contains `id`, `relative_path`, `sha256`, `title`, `primary_role`, `selection_score`, and `selection_basis`. Use stable IDs such as `A1`; hashes must be lowercase SHA-256. The optional `secondary_roles` list, when present, is read by the validator and must use the same role vocabulary as `primary_role` (`empirical-results`, `method-mechanism`, `discussion-boundaries`, `introduction-framing`, `artifact-reproducibility`, `venue-register`); it counts toward role coverage. `artifacts` keys are `inventory`, `selection`, `profile`, `contract`, `metrics`, and `target_audit`, each mapped to its fixed filename.

Allowed lifecycle statuses:

- `CORPUS_INVENTORIED`
- `ANCHORS_FROZEN`
- `PROFILE_SAVED`
- `TARGET_AUDITED`
- `STYLE_APPLIED`
- `INSUFFICIENT_REPOSITORY_STYLE_CORPUS`
- `BLOCKED_AUTHORITY_AMBIGUOUS`

The last two are not complete profiles.

### `CORPUS-INVENTORY.json`

Use schema `paper_style_inventory_v1`. Keep all frozen candidates, including exclusions and duplicates. Enrich helper output with human-reviewed `source_class`, `eligibility`, and `decision_reason`; do not discard unresolved cases. A selected source uses `source_class: external_published_full_text` and `eligibility: eligible`; all other values remain explicit rather than being inferred by the validator.

### `SELECTION-REPORT.md`

First line: `<!-- paper-style-profiler: selection-report-v1 -->`

Explain the frozen frame, selected anchors, excluded near-matches, complementarity, and non-transferable features.

### `LANGUAGE-STYLE-PROFILE.md`

First line: `<!-- paper-style-profiler: language-profile-v1 -->`

Use the full language protocol. Keep argument architecture out of the language findings.

### `WRITING-CONTRACT.md`

First line: `<!-- paper-style-profiler: writing-contract-v1 -->`

Organize rules under these semantic sections in the repository's document language:

- preserve: claims, evidence, terminology, citations, and locked material;
- prefer: high-confidence shared and role-specific language behaviors;
- avoid: corpus-derived anti-patterns and non-transferable source features;
- validation: semantic invariants, whole-document pattern checks, and stale-state checks.

Every positive rule should name its applicable section or rhetorical role. Avoid generic commands such as “write clearly” or numeric word-count quotas.

### `metrics.json`

Use schema `paper_style_language_metrics_v1`. Store derived counts and rates only. The `papers` keys must equal the selected anchor IDs. Do not store raw sentences, quotations, or temporary paths.

### `TARGET-GAP-AUDIT.md`

Required only when state is `TARGET_AUDITED` or `STYLE_APPLIED`. First line:

`<!-- paper-style-profiler: target-gap-audit-v1 -->`

Record target hash, section/locations, observed mismatch, contract rule, confidence, semantic risk, and disposition. Separate actionable language issues from intentional claim-boundary language.

## Refresh logic

At invocation, compare state with current files:

1. Anchor hash mismatch: profile is stale; refresh extraction.
2. Anchor missing: profile is stale; resolve source before writing.
3. Target hash mismatch: target audit is stale; anchors need not be reselected unless genre or venue also changed.
4. Material new eligible corpus: report possible reselection and refresh when requested or when the old complementarity no longer holds.
5. Venue/genre/claim-ceiling change: rerun selection judgment even when PDFs are unchanged.

Do not silently replace prior rationale. Version control provides history; the new state records refresh reason and prior profile identifier when available.

## Validation command

Run the bundled validator with the chosen bundle and authoritative repository root. A complete profile must pass without errors:

```bash
python3 scripts/validate_style_bundle.py BUNDLE_DIR --repo-root REPOSITORY_ROOT
```

Incomplete states may validate their available artifacts but must remain explicitly non-usable for writing.
