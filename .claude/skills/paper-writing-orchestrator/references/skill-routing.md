# Skill Routing

Read this reference when the next paper stage needs a companion skill. Check the
skills actually available in the current environment before routing.

| Need | Preferred skill | Boundary |
|---|---|---|
| Diagnose an "incremental" verdict, name the problem, set why-now, decide Figure 1 judgment or main versus appendix allocation | `$paper-framing` (`reader-visibility.md`) | Visibility edits stay inside the claim ceiling; they do not replace missing difference or evidence |
| Decide the research stage (R0-R5), check R gates, record a rollback or a handoff | `$research-pipeline` | Owns the R stages above this orchestrator's S0-S7; this orchestrator runs inside R4 and R5 |
| Build the story spine, decide Figure 1, write the six-step introduction and Answer-to-RQ boxes, or diagnose a draft that reads like a lab report | `$paper-storytelling` | Narrative order and emphasis only; claim strength stays with the ledger |
| Build, refresh, audit, or apply the repository style contract | `$paper-style-profiler` | Language only; argument structure, claims, and terminology are untouched |
| Decide figure versus table and the representation family under an evidence contract | `$publication-chart-skill` | Hands data plots to `$scientific-visualization` and tables to its own `pubtab` branch |
| Read, explain, compare, position, or run a literature checkpoint | `$paper-reading` | Record whether reading occurred before protocol freeze or after a finding; post-finding context cannot be promoted to prospective design |
| Create or audit a data-backed publication plot | `$scientific-visualization` | Data, transformations, uncertainty, and final export must be traceable |
| Create or audit an editable method, architecture, protocol, or workflow diagram | `$drawio-skill` | Terminology and modeled relationships must come from authoritative manuscript or method sources |
| Create, convert, preview, or audit a publication table | Table branch of `$publication-chart-skill` (`pubtab`) | Every displayed value must map to a source; keep the table as editable text |
| Draft or minimally revise academic prose | `$academic-humanizer` | Claims and terminology must already be grounded |
| Assess framing, evidence chain, experiments, or submission readiness for the target venue (graded L1/L2/L3) | `$paper-review` with the venue profile named in `paper/VENUE_PROFILE.md` | Read-only unless edits are explicitly requested; an unprofiled venue uses its generic rubric |
| Review a security paper | `$paper-review` with the venue profile from `paper/VENUE_PROFILE.md`; when the venue has no profile under its `references/venues/`, also read `security-venue-review.md` as a supplement | Do not substitute an economics referee rubric |
| Inspect final PDF layout | `$pdf` | Visual/mechanical QA only |
| Create or refactor a requested notebook | `$jupyter-notebook` | Do not force notebooks on ordinary plotting work |
| Create a requested XLSX/CSV workbook | `$Spreadsheets` | Spreadsheet artifact, not a LaTeX paper table by default |
| Produce a paper talk or academic deck | `$academic-paper-ppt` or repository-selected presentation skill | Separate deliverable after manuscript claims are stable |
| Track a durable task DAG | `$task-forest` | Only when the user requests task-forest tracking |
| Transfer context to a fresh session | `$session-handoff-prompt` | Handoff only; it does not perform paper work |

## Routing rules

1. Use the narrowest skill that owns the current task.
2. Do not invoke the orchestrator merely to read one paper, polish one paragraph,
   create one isolated figure or table, or inspect one PDF.
3. When the request is part of an active end-to-end workflow, keep the
   orchestrator as stage owner and let the companion own its specialized work.
4. Load only the selected companion's instructions and relevant references.
5. A companion's successful output returns to the orchestrator for its stage
   gate; it does not advance the paper automatically.
6. Repository `AGENTS.md` or `CLAUDE.md`, user instructions, and frozen evidence contracts take
   precedence over generic routing defaults.
7. Use the versions recorded in `external-skill-locks.md`. Upstream popularity
   or a successful render is not evidence that a scientific comparison is
   valid or that a venue accepts the artifact.
8. Probe optional runtimes before use. Do not let an external skill silently
   mutate a repository Python environment, lockfile, or TeX installation.
9. When `research/STATE.md` exists, `$research-pipeline` owns the R stage: it
   decides whether the paper is in R4 or R5 at all, and a mismatch between an
   inherited artifact (FRAMING, STORY_SPINE, ledgers) and current evidence is
   recorded there as a rollback, not patched here.

## Explicit exclusions

- Do not route this workflow to `$review-paper`, an economics-journal referee
  rubric that may be installed outside this repository; the in-repo graded
  review is `$paper-review`.
- Do not route new work to the retired local `$paper-figure` or `$paper-table`
  implementations. Their rendering logic has been replaced by installed
  upstream skills.
- Do not use image generation to create data-backed results, axes, points,
  uncertainty intervals, or quantitative comparisons.
- Do not use a PDF or spreadsheet success check as a substitute for scientific
  review.
- Do not run `$innovation-explore` from inside this orchestrator; direction
  finding (R0) precedes the manuscript workflow and has its own stage lock.
