# Workflow

## Default decision order

1. Identify the scientific communication goal.
2. Probe the environment and available assets lightly.
3. Decide whether the evidence should be a figure, a table, or a paired figure+table deliverable.
4. Choose the strongest representation family.
5. Route to `pubfig`, `pubtab`, or both.
6. For figures, hand the chosen representation to `scientific-visualization` for integrity, accessibility, physical-size, provenance, and delivered-file checks when that skill is available.
7. Produce the smallest runnable implementation.
8. Specify export outputs explicitly.
9. Run publication QA.
10. Propose revisions if the result is weak.

## Responsibility and handoff

| Stage | Owner | Output |
|---|---|---|
| Evidence contract | `publication-chart-skill` | claim, unit of analysis, metric direction, missingness, uncertainty basis |
| Artifact choice | `publication-chart-skill` | figure, table, or paired deliverable and representation family |
| Figure construction | `pubfig` or project plotting code | runnable figure source |
| Figure integrity and delivery | `scientific-visualization` | honest encoding, accessible redundancy, target dimensions, provenance, rendered-file inspection |
| Table construction and QA | `pubtab` plus this skill | publication table, preview, and table-specific QA |

The handoff is one-way: do not repeat chart selection inside the figure-integrity stage. If `scientific-visualization` is unavailable, retain the same integrity checks locally rather than treating `pubfig` output as automatically publication-ready.

## Handoff checklist

For every task, try to make these explicit:

- claim the artifact is supposed to support
- data shape and grouping structure
- target audience or venue expectations
- figure vs table role
- exact output filenames and formats
- whether the artifact is final, draft, or revision
- whether the current environment can execute the proposed route immediately

## Delivery contract

A strong response should make clear:

- which artifact type was chosen,
- why it was chosen,
- which tool owns each artifact,
- what the first runnable command/code path is,
- what output files should be produced,
- what still needs user input or upstream data.

## Default output priorities

Prioritize in this order:

1. clarity of claim
2. correct artifact type
3. minimal runnable implementation
4. publication-ready export
5. QA and revision guidance

## Graceful degradation when tools are missing

If `pubfig` or `pubtab` is not installed:

- keep the workflow going,
- provide installation guidance,
- provide pseudocode or draft commands,
- specify the recommended artifact structure,
- preserve the QA and revision guidance.

## Figure / table split rules

Use a **figure** when the reader needs to quickly perceive:

- trend
- distribution shape
- relationship
- calibration or diagnostic behavior
- composition or hierarchy
- visual comparison across a moderate number of groups

Use a **table** when the reader needs:

- exact numbers
- many metrics side by side
- benchmark grids
- ablation matrices
- appendix-style detail
- reproducible value lookup

Use **both** when:

- the figure carries the visual claim,
- the table preserves exact values,
- or the paper section benefits from a fast visual summary plus precise numeric evidence.
