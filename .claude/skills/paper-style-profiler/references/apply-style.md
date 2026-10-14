# Applying a Saved Style Contract

Use this protocol only for an explicit writing or revision request. A profile-extraction request alone does not authorize manuscript edits.

## Preconditions

1. Load `STYLE-STATE.json` and validate the bundle.
2. Verify selected source hashes and the target identity.
3. Read repository claim/evidence ledgers, terminology rules, locked text, and applicable authoring instructions.
4. If the target changed, refresh the target audit. If an anchor changed, refresh the profile.
5. Define the exact edit scope: paragraph, section, or manuscript.

## Semantic preservation ledger

Before changing prose, identify:

- factual propositions and numbers;
- positive, negative, and unresolved findings;
- modality and uncertainty;
- causal versus correlational relations;
- population, version, configuration, and threat-model scope;
- baselines and comparison direction;
- citations and attribution;
- manuscript-wide terminology identities;
- text that is intentionally locked.

After revision, verify each item. If a style rule conflicts with one, the ledger wins.

## Revision method

- Revise for rhetorical function, not surface resemblance. Transfer patterns such as evidence-first results, clear agency, bounded interpretation, or lighter clause chaining; never transfer distinctive sentences.
- Prefer small, reviewable edits. Do not synonym-cycle stable technical terms.
- Remove formulaic section openers, empty importance claims, repetitive previews, mechanical triads, and process-leaking prose only when the source meaning remains intact.
- Reduce legalistic density by splitting unrelated qualifications or moving a boundary next to the claim it governs. Do not delete necessary limitations.
- Vary document-level patterns based on rhetorical need, not randomness.
- Keep negative results, abstentions, unresolved cases, and counterevidence visible.
- Do not introduce facts, examples, citations, author experiences, novelty claims, or acceptance claims absent from the source manuscript.

When the `academic-humanizer` skill is available and the user asks for de-formulaic academic revision, its semantic-preservation and manuscript-wide terminology checks may be used together with this repository contract. The saved profile supplies project-specific language evidence; it does not relax that skill's boundaries.

## Post-edit checks

Perform both local and global checks:

- proposition, number, polarity, modality, scope, and citation preservation;
- terminology identity across all affected files;
- repeated sentence openings and paragraph templates across the document;
- section-appropriate agency, verbs, tense, and transitions;
- claim ceiling and evidence traceability;
- build or render checks required by the repository.

Update `TARGET-GAP-AUDIT.md` with resolved, retained, and rejected suggestions. A rejected style suggestion is a valid outcome when it would distort evidence or terminology.
