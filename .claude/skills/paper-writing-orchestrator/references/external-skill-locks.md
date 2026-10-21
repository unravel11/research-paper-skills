# External Figure, Diagram, and Table Skill Locks

These upstream packages own figure, diagram, and table implementation. The
paper-writing orchestrator owns only stage routing, repository authority,
evidence compatibility, claim ceilings, venue selection, and manuscript-wide
consistency.

## Locked sources

All of these are bundled in this repository under `.claude/skills/` and were
taken from the pinned commit. The notes column says whether the bundled copy
is byte-identical to upstream or carries local changes; every local change is
listed in the repository's `THIRD_PARTY_NOTICES.md` together with the
copyright lines and license texts.

| Route | Installed skill | Repository path | Commit | License | Notes |
|---|---|---|---|---|---|
| Data-backed publication plots | `$scientific-visualization` | `K-Dense-AI/scientific-agent-skills/skills/scientific-visualization` | `48dc1cf173f01aea114a62d634066f6b272aaaf1` | MIT | modified; see THIRD_PARTY_NOTICES.md |
| Editable method and architecture diagrams | `$drawio-skill` | `Agents365-ai/drawio-skill/skills/drawio-skill` | `2ee141e0ff183ce76dc405370aeb142c6961aa45` | MIT | unmodified |
| Publication tables | Table branch of `$publication-chart-skill` | `Galaxy-Dawn/claude-scholar/skills/publication-chart-skill` | `2f7766fd541a723d4ddc6230b3277f948d61b093` | MIT | modified; see THIRD_PARTY_NOTICES.md |
| Fact-preserving academic prose revision | `$academic-humanizer` | `dongshuyan/compass-skills/skills/academic-humanizer` | `1b2e556ce6f293ba12e95e18d51995d6a969d52f` | MIT | modified; see THIRD_PARTY_NOTICES.md |
| Durable task DAG | `$task-forest` | `dongshuyan/compass-skills/skills/task-forest` | `1b2e556ce6f293ba12e95e18d51995d6a969d52f` | MIT | unmodified |
| Fresh-session handoff | `$session-handoff-prompt` | `dongshuyan/compass-skills/skills/session-handoff-prompt` | `1b2e556ce6f293ba12e95e18d51995d6a969d52f` | MIT | unmodified |

Referenced but not bundled: `$pdf` (Anthropic's document skill, distributed
under Anthropic's own license, so it is not redistributed here), and the
optional `$jupyter-notebook`, `$Spreadsheets`, `$academic-paper-ppt` and
`$review-paper` routes. Without them the corresponding route is skipped.

The table route uses `pubtab`. Version `1.0.1` passed the isolated smoke test on
2026-08-19. Treat its package version and executable availability as a runtime
dependency to probe, not as permission to modify a paper repository's
environment.

## Route boundaries

- Data plot: use `$scientific-visualization`; retain source data,
  transformations, uncertainty definitions, vector output, preview, and final
  visual inspection.
- Schematic: use `$drawio-skill`; retain `.drawio` source plus requested
  exports and inspect the rendered result. For manuscript PDF export, use a
  cropped page when supported and verify the rendered page; an uncropped
  draw.io PDF can retain a full document page around the diagram.
- Table: use the `pubtab` branch of `$publication-chart-skill`; retain editable
  LaTeX and its structured input. Use the manuscript's existing class and
  typography rather than importing a generic publisher template. Preview the
  table body first, then compile the final float, caption, and label inside the
  authoritative manuscript; `pubtab preview` is not a substitute for that
  integration build.
- Mixed plot and table: route each artifact separately unless the user
  explicitly requests the upstream paired workflow.

## Safety and currency

- Verify current official venue instructions for the exact journal, article
  type, and submission phase before claiming format compliance.
- Do not generate or alter quantitative evidence with an image-generation
  model.
- Do not install Python packages into a repository interpreter, alter a
  lockfile, or bootstrap TeX automatically without explicit authorization.
- A successful export, preview, or compile proves only the checked mechanical
  condition. It does not establish scientific validity, venue compliance,
  submission readiness, or acceptance.
- Upstream updates require a fresh source review, a new pinned commit, and
  regression checks before replacing these locks.
