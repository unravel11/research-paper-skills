# Provenance-Aware Production Patterns

Use this reference after the evidence contract, target medium, and approximate final width are known. It adds production-tested layout ideas without turning one repository's visual identity into a universal scientific style.

## Evidence basis and reuse boundary

These patterns were reviewed on 2026-08-20 against Chen Liu's public [`figures4papers`](https://github.com/ChenLiu-1996/figures4papers) repository at commit [`6790a93af3552539d955d77181c818916e1700b7`](https://github.com/ChenLiu-1996/figures4papers/commit/6790a93af3552539d955d77181c818916e1700b7). The repository pairs project-specific Python scripts with rendered outputs from several papers, which makes it useful as a pattern source.

The repository did not declare a license at the reviewed commit. Do not copy or redistribute its code, palettes, or rendered assets. The examples below are independently written Matplotlib patterns based on general layout ideas. Link to the original repository when its examples informed a decision.

The source also documents proposed helpers that are not shipped as a shared implementation. Do not assume functions named `make_grouped_bar`, `make_trend`, or `finalize_figure` exist merely because its reference pages specify them.

## Pattern router

| Need | Candidate pattern | Reject or reconsider when |
|---|---|---|
| A shared legend covers data or repeats across panels | Dedicated legend axis | Direct labels or a compact figure-level legend are clearer |
| A small comparison needs exact values at a glance | Conditional value labels | Labels collide with uncertainty, there are many bars, or a table is the real deliverable |
| Several panels must fit a journal column or page | Width-derived layout | A fixed ultra-wide canvas would only postpone downscaling problems |

These patterns do not override the zero-baseline, uncertainty, missing-data, color, accessibility, or export rules in `SKILL.md` and `references/publication_guidelines.md`.

## 1. Dedicated legend axis

Use a separate legend axis when a shared legend is necessary and would otherwise overlap data or consume inconsistent space across panels. First consider direct labels and `fig.legend`; the extra axis is useful when the legend is structurally large.

```python
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(178 / 25.4, 62 / 25.4), layout="constrained")
axes = fig.subplot_mosaic(
    [["metric_a", "metric_b", "legend"]],
    width_ratios=[1, 1, 0.55],
)

for label, values in series.items():
    axes["metric_a"].plot(x, values["a"], label=label)
    axes["metric_b"].plot(x, values["b"], label=label)

handles, labels = axes["metric_a"].get_legend_handles_labels()
axes["legend"].set_axis_off()
axes["legend"].legend(handles, labels, loc="center", frameon=False)
```

Review at final size. The legend order must follow the visual or scientific order, and color must have a redundant cue where series identity matters.

## 2. Conditional bar-value labels

Use value labels for a small number of bars when exact lookup is part of the communication goal. Preserve a zero baseline for ordinary bars. Do not place labels on top of error bars or significance annotations, and do not label every mark in a dense panel.

```python
bars = ax.bar(categories, estimates, yerr=intervals, capsize=3)
ax.set_ylim(bottom=0)
ax.bar_label(
    bars,
    labels=[f"{value:.2f}" for value in estimates],
    padding=5,
)
ax.set(ylabel="Score (unit)")
```

If uncertainty extends above the bar, either offset labels using rendered artist extents, move exact values to a companion table, or omit the labels. A bar label never establishes significance or replaces the caption's definition of the interval and replication unit.

## 3. Width-derived multi-panel layout

Start from the destination width, not a visually comfortable arbitrary canvas. Convert millimetres to inches, choose the smallest panel width that remains readable, then decide columns and rows.

```python
from math import ceil
import matplotlib.pyplot as plt

target_width_mm = 178
panel_count = 4
minimum_panel_width_mm = 82

columns = max(1, min(panel_count, target_width_mm // minimum_panel_width_mm))
rows = ceil(panel_count / columns)
width_in = target_width_mm / 25.4
height_in = rows * 58 / 25.4

fig, axes = plt.subplots(
    rows,
    columns,
    figsize=(width_in, height_in),
    layout="constrained",
    squeeze=False,
)
```

The numeric thresholds are task inputs, not universal constants. Derive them from label length, panel content, article type, and a rendered final-size check. If the target is unknown, mark the layout provisional.

## Provenance case card

When a public production example materially influences a figure, record a small case card in the project notes or manifest:

- communication goal and scientific claim;
- source example URL and reviewed commit/date;
- pattern borrowed at the idea level;
- data and transformations used in the new figure;
- target physical dimensions and output formats;
- rendered-output inspection result;
- differences from the source and why they were necessary.

This card is provenance for a design decision. It does not imply that publication in a venue validates the encoding, accessibility, or scientific conclusion.

## Rejected defaults

Do not generalize these observed house-style choices:

- assigning blue to the proposed method and red to baselines;
- automatically tightening bar-chart limits to magnify differences;
- fixed ultra-wide figure sizes or fixed large font sizes;
- universal `tight_layout()` or `bbox_inches="tight"` export;
- default TeX/Helvetica dependencies;
- radar, polar, or decorative 3D as a style signature.

Use the current skill's evidence, accessibility, and exact-export rules instead.
