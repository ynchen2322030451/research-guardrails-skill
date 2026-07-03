---
name: research-guardrails
description: Use this skill for research-project tasks involving server operations, deletion/cleanup, data recovery, sync-delete, overwrites, frozen result artifacts, or any agent action where research data safety matters. It enforces non-negotiable rules for protecting data and avoiding unsafe destructive commands.
---

# Research Guardrails

Use this skill before acting on research data, results, scripts, figures, manuscripts, or server files. The default posture is: protect irreplaceable data first, preserve canonical evidence, and downgrade unsupported claims.

## Setup Defaults

This skill works without setup. If no project profile exists, use conservative defaults:

- use the default protected/private path lists in `references/configuration.md`
- use move-to-quarantine instead of permanent deletion
- require file-backed evidence for all quantitative claims
- block recursive/quiet/cross-shell deletion until reviewed

When setup matters, ask the user to verify at most three items:

1. Which directories contain irreplaceable data?
2. Which result directory or file is currently authoritative?
3. Which private/confidential paths must never be uploaded?

Use `project-profile.example.yaml` as a small optional template; do not require every field to be filled.
For a small interactive setup, run `python scripts/init_project_profile.py` from the skill directory.

## First Response

When this skill triggers, state the operation class before touching files:

- **text-only**: manuscript wording, notes, captions, no result generation.
- **plotting-only**: figure rendering from existing data.
- **postprocessing-only**: derives summaries from saved CSV/JSON/NPZ without changing experiments.
- **experiment-changing**: training, HF reruns, posterior reruns, new data generation, or anything that changes saved scientific results.
- **destructive-risk**: delete, move, overwrite, cleanup, sync with deletion, permission changes, remote server shell, or disk-space recovery.

If the class is unclear, treat it as destructive-risk until proven otherwise.

## Non-Negotiable Iron Rules

1. Never modify raw source data.
2. Never overwrite frozen/canonical artifacts unless the user explicitly authorizes a new run tag or OUT_DIR.
3. Never run recursive deletion, cleanup, or sync-delete commands from an agent without an explicit path audit and a recoverable backup.
4. Never trust a path variable in a destructive command unless the command itself asserts non-empty values.
5. Never rely on current working directory for destructive commands; use explicit absolute paths.
6. Never run `git add -A` in this project. Use precise paths.
7. Never commit or upload confidential folders, secrets, credentials, SSH keys, private machine config, or restricted unpublished material.
8. Never describe approximate retrieval, cached lookup, surrogate output, or indirect validation as an exact rerun/measurement.
9. Never report a quantitative manuscript claim unless it is backed by a named local file or explicitly marked 待核实.
10. Never mix result tracks, model versions, datasets, or rerun batches without saying which track is active.

## Destructive Command Gate

Before any destructive-risk operation:

1. Read `references/data-safety.md`.
2. Identify target path, path owner, artifact class, and backup status.
3. Run a dry-run/listing version first (`find ... -print`, `rsync --dry-run`, `git status --short`, etc.).
4. If shell commands are proposed, run:

```bash
python .claude/skills/research-guardrails/scripts/check_command_safety.py '<command>'
```

5. Stop if the checker reports `BLOCK`.
6. For allowed deletion, prefer moving to a quarantine directory over permanent deletion.

## Evidence Gate

Before manuscript claims, figures, tables, recovery reports, or rebuttal text:

1. Read `references/evidence-ledger.md`.
2. Choose exactly one project-defined result track from the evidence ledger or project profile.
3. Bind every printed number to a local file path.
4. If the file is absent, write 待核实 or downgrade the claim.
5. Do not turn uncertain intervals, failed diagnostics, incomplete runs, or exploratory outputs into stable conclusions.
6. For figures, translate internal column/model names into paper-facing language and respect the project's figure-language rules.

## Recovery Gate

For data-loss, missing artifact, server failure, or "what do we still have?" tasks:

1. Read `references/recovery-playbook.md`.
2. Work read-only first: inventory local files, Git status, Git history, and remote-tracked status.
3. Classify assets as:
   - **A**: local + GitHub, safe
   - **B**: local only, push/backup immediately
   - **C**: server raw lost but local derived products exist
   - **D**: canonical missing and must regenerate
   - **E**: exploratory/later-track, recover only if adopted
4. Preserve local-only irreproducible data before analysis polish.
5. Do not attempt server recovery commands unless the user explicitly requests server-side work.

## Group Sharing

This skill is designed to live in a GitHub repo under `.claude/skills/research-guardrails/`. For a new user or machine, copy that folder into the repo's `.claude/skills/` directory. Claude Code can invoke it as `$research-guardrails`; Codex can read the same `SKILL.md` as project rules.

For group-wide reuse, keep project-specific evidence paths in `references/evidence-ledger.md` or a copied project profile, and keep general safety rules in `references/data-safety.md`. When adapting to a new project, replace only the project-specific profile/ledger.

## References

- Read `references/data-safety.md` for deletion, cleanup, remote shell, backup, and Git guardrails.
- Read `references/evidence-ledger.md` for project result tracks and manuscript claim rules.
- Read `references/configuration.md` for the recommended default profile and three-question setup.
- Read `project-profile.example.yaml` when setting up the skill for a new project.
- Read `references/recovery-playbook.md` for data-loss triage and recovery prioritization.
