# Evidence Ledger

Use this reference when writing, plotting, auditing, or deciding which results support a claim.

## Result Tracks

Choose one active track before quoting numbers. Replace the examples below with project-specific tracks, paths, and approved terminology. If the project has a filled profile file, treat it as the source of truth.

### Track Template

Purpose: describe what this result track is for, such as main manuscript, robustness check, exploratory rerun, external validation, or legacy comparison.

Known evidence locations:

- Dataset/source files: `TODO / 待填写`
- Split/sample metadata: `TODO / 待填写`
- Frozen model/artifact directory: `TODO / 待填写`
- Evaluation metrics: `TODO / 待填写`
- Prediction/summary tables: `TODO / 待填写`
- Figure source data: `TODO / 待填写`
- Manuscript source: `TODO / 待填写`

Approved headline numbers:

- `metric_name`: value, unit, source file, date
- `metric_name`: value, unit, source file, date

Known limitations:

- `TODO / 待填写`
- `TODO / 待填写`

Use this track when:

- `TODO / 待填写`

## Claim Rules

- Evidence: direct file-supported result.
- Interpretation: explanation inferred from evidence.
- Limitation: uncertainty, missing file, incomplete run, or noncanonical track.

Every scientific paragraph should keep these distinct.

If a number cannot be traced to a file:

- Write 待核实 in Chinese drafts.
- Write "pending audit" or remove the number in English/figures.
- Prefer qualitative phrasing over invented precision.

## Figure Vocabulary

Do not show raw identifiers in manuscript figures.

- Replace code-level dataset names with reader-facing names.
- Replace internal model IDs with descriptive scientific names.
- Replace raw column names with axis-label-ready terms and units.
- Keep a project-specific forbidden-term mapping in the project profile.

Rendered figure panels, legends, axes, and embedded captions should follow the target venue language and font constraints. If a plotting library cannot render a language reliably, use venue-language placeholders such as "N/A" or "pending audit" instead of broken glyphs.

## Uncertainty Rules

- Intervals crossing a null or decision boundary cannot support a stable directional claim.
- Main text should focus on robust primary outputs; exploratory sweeps belong in appendix unless explicitly requested.
- Do not compute deltas, ratios, or paired comparisons unless the project profile defines the valid pairing.
