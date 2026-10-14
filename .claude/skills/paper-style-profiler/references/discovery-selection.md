# Discovery and Selection Protocol

Use this protocol only after repository authority, manuscript target, and output location are known.

## Candidate inventory

Search narrowly and record every discovered PDF before close reading. Prefer `rg --files -g '*.pdf'` in repository-defined literature, paper, artifact, or reference directories. Do not recursively inspect dependency trees, caches, build directories, cloned targets, raw datasets, or unrelated archives.

For each candidate record:

- repository-relative path;
- normalized title and available bibliographic metadata;
- SHA-256 and page count;
- extraction status and approximate readable-text coverage;
- source class and eligibility decision;
- duplicate relationship by hash, title, DOI, or obvious version lineage;
- exclusion reason when ineligible.

The current manuscript, its previous drafts, author rebuttals, generated literature notes, slide decks, theses, and reviewer reports are not external model papers. A preprint and camera-ready version of the same work count as one source.

## Eligibility gates

A paper is eligible only when all are true:

1. a published paper or stable public preprint can be identified;
2. enough full text is extractable to analyze multiple sections;
3. its research genre or rhetorical work is relevant to the target manuscript;
4. its language quality is suitable for close analysis;
5. its normal claim behavior does not invite systematic overclaiming in the target;
6. it adds a role not already overrepresented in the anchor set.

Metadata uncertainty may remain `unresolved`; do not convert it to eligibility by assumption.

## Scoring rubric

Score eligible candidates with explicit evidence. Use totals to organize judgment, not automate it.

| Dimension | Range | Question |
|---|---:|---|
| Research-genre fit | 0–5 | Does it perform a comparable kind of empirical, systems, security, or software-engineering study? |
| Evidence-shape fit | 0–5 | Does it report evidence with similar units, baselines, negative cases, uncertainty, or scope limits? |
| Rhetorical-task fit | 0–5 | Does it model sections the target actually needs help writing? |
| Language quality | 0–5 | Is the prose precise, readable, and internally consistent across sections? |
| Claim-ceiling compatibility | 0–5 | Can its language be transferred without inflating certainty, causality, prevalence, or generality? |
| Section coverage | 0–3 | Are the needed sections available and extractable? |
| Extraction reliability | 0–2 | Is text extraction sufficiently complete and clean? |

Maximum: 30. Do not set a universal pass threshold. A candidate with a claim-ceiling conflict cannot be rescued by its total score.

## Complementary anchor set

Select three to five unique papers. Assign one primary role to each, with optional secondary roles:

- `empirical-results`
- `method-mechanism`
- `discussion-boundaries`
- `introduction-framing`
- `artifact-reproducibility`
- `venue-register`

At minimum, the set should cover empirical results, method/mechanism, and discussion/boundary language. If one paper covers two roles, the corpus still needs three unique works so the profile is not a disguised single-author imitation.

## Selection report

The report starts with:

`<!-- paper-style-profiler: selection-report-v1 -->`

Then document:

1. target manuscript and venue/genre;
2. frozen candidate frame and exclusions;
3. selected anchors with scores, roles, hashes, and concise evidence;
4. excluded near-matches and why they lost;
5. complementarity rationale;
6. unresolved metadata or human judgments;
7. features that must not transfer, such as novelty superlatives, causal verbs, prevalence language, or venue-specific formatting.

If fewer than three papers survive, create only the incomplete-state artifacts and state what kind of missing source would close the gap. Do not browse automatically.
