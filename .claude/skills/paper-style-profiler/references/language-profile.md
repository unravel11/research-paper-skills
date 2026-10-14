# Language Profile Protocol

This protocol extracts linguistic behavior. It does not infer scientific quality from prose and does not treat argument architecture as language style.

## Evidence levels

Label each observation as one of:

- `shared`: visible across most anchors and more than one section;
- `role-specific`: useful for a named section or rhetorical task;
- `paper-specific`: distinctive but not transferable by default;
- `uncertain`: may be an extraction artifact or too sparse to generalize.

Quantitative metrics support inspection; they do not prove a rule. Qualitative rules need locations across multiple papers, but saved artifacts should use short paraphrased evidence rather than source sentences.

## Required language dimensions

### Agency and grammatical subjects

Identify when clauses foreground authors (`we`), the study, the system, the data, the result, prior work, or a limitation. Explain what each subject choice accomplishes. Do not reduce this to a first-person frequency.

### Voice and verb families

Distinguish active and passive constructions and map common verb functions:

- research action: design, collect, implement, evaluate, compare;
- evidence: observe, find, measure, show, report;
- interpretation: suggest, indicate, imply, explain;
- comparison: outperform, differ, remain, increase, decrease;
- boundary: limit, restrict, focus, condition, exclude;
- obligation or uncertainty: must, should, may, might, could.

Record which verbs are avoided when evidence is correlational, conditional, incomplete, or negative.

### Tense, aspect, and modality

Describe section-level tense patterns: established knowledge, method actions, observed results, and present interpretation. Track hedges and modal force together with the claims they govern; never add or remove a hedge without checking semantic effect.

### Sentence construction

Measure sentence and clause length, but analyze how information is packed: main-clause-first versus setup-first, coordination versus subordination, definition patterns, contrast placement, parenthetical load, and sentence openings. Flag long legalistic chains separately from necessary technical qualification.

### Discourse relations

Classify transitions by function rather than copying surface phrases:

- contrast or concession;
- cause or consequence;
- addition or enumeration;
- evidence or example;
- interpretation;
- limitation or scope;
- local preview or recap.

Note when relations are carried by syntax instead of explicit transition words.

### Punctuation and local rhythm

Inspect semicolons, colons, parentheses, dashes, lists, equations, and citation placement. Describe paragraph rhythm as opening claim or context, evidence/development, interpretation, and boundary/transition. Numeric rates are descriptive ranges, never punctuation targets.

### Section-specific register

Build separate rules for:

- Introduction: problem setup, gap, contribution, and bounded motivation;
- Background/Related Work: attribution and comparison without straw-manning;
- Method/System: operational verbs, definitions, assumptions, and reproducibility detail;
- Results: question-answer structure, numerical comparisons, negative evidence, and uncertainty;
- Discussion/Validity: interpretation, alternatives, scope limits, and non-generalization;
- Conclusion: evidence-sized synthesis without new claims.

## Profile artifact

Start the profile with:

`<!-- paper-style-profiler: language-profile-v1 -->`

Include:

1. corpus boundary and extraction quality;
2. high-confidence shared patterns;
3. role- and section-specific patterns;
4. paragraph and sentence rhythm;
5. terminology and comparison behavior;
6. negative-result and limitation language;
7. paper-specific features not to generalize;
8. non-transferable features that conflict with the target's claim ceiling;
9. descriptive metrics with ranges and caveats;
10. unresolved judgments.

The profile must explicitly state that it models aggregate language, contains no reusable source sentences, and does not certify human authorship or publication quality.
