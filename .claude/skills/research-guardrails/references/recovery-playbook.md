# Recovery Playbook

Use this reference for data-loss triage, missing result directories, server deletion incidents, or "what do we still have?" tasks.

## Immediate Response

1. Stop destructive activity.
2. Do not run cleanup, repair, or recovery writes on the affected disk unless the user explicitly asks.
3. Inventory local copies, Git status, Git history, GitHub/remote tracking, and external disks.
4. Preserve local-only irreproducible assets first.

## Asset Classes

- **A: Safe** - local + GitHub/remote copy exists.
- **B: Local-only risk** - local copy exists, remote missing. Push or cold-backup immediately.
- **C: Server raw lost, derived local exists** - raw intermediate gone but frozen CSV/NPZ/VTU/workbooks exist; manuscript may still be supported.
- **D: Canonical missing** - missing artifact is needed for reproducibility or future inference; regenerate or recover from backup.
- **E: Exploratory** - not adopted in current manuscript; recover only if user decides to use it.

## Common Data-Loss Lessons

Common root causes include empty path variables, inherited working directories, cross-shell quoting changes, generated scripts that were not inspected, quiet/force delete flags, and agents escalating after an initial deletion failure.

Preventive rules:

- Empty path must abort, not default.
- Generated scripts must be printed and inspected before execution.
- Destructive jobs must have dry-run output.
- Cross-shell destructive wrappers must be blocked or separately reviewed.
- After one destructive failure, stop and ask for a fresh exact-command review.
- SSH failure after deletion can mean `.ssh/authorized_keys` was deleted; verify physically.
- Commit is not enough; push and verify remote state.

## Local Inventory Commands

Read-only checks:

```bash
git status --short --untracked-files=all
git log --oneline --decorate -20
git log --oneline --decorate origin/$(git branch --show-current)..HEAD
find code -maxdepth 5 -type f \( -name '*.csv' -o -name '*.json' -o -name '*.npz' -o -name '*.pt' -o -name '*.pkl' -o -name '*.vtu' -o -name '*.xlsx' \) | sort
```

Dataset or split sanity template:

```bash
python - <<'PY'
import csv, json, pathlib
for p in ["path/to/dataset.csv"]:
    if not pathlib.Path(p).exists():
        continue
    with open(p, newline="", encoding="utf-8-sig") as f:
        r = csv.reader(f); h = next(r); n = sum(1 for _ in r)
    print(p, n, len(h))
for p in pathlib.Path(".").glob("**/split_meta.json"):
    try:
        j = json.load(open(p))
    except Exception:
        continue
    if "n_total" in j:
        print(p, j.get("n_total"), j.get("n_train"), j.get("n_val"), j.get("n_test"))
PY
```

## Recovery Priorities

1. Raw source data and sample/split definitions.
2. Frozen model, calibration, or processing artifacts.
3. Frozen predictions, metrics, and summary tables.
4. Expensive posterior/simulation/validation samples and summaries.
5. External validation summaries and archived run outputs.
6. Source-data workbooks and figure data.
7. Manuscript source, figure scripts, and review-response records.

If current manuscript numbers are already backed by local frozen downstream products, do not rerun expensive experiments just to reduce anxiety. Document the evidence path instead.
