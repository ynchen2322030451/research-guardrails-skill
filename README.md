# Research Guardrails Skill

A reusable AI-agent guardrail skill for research projects. It helps Claude Code, Codex, and other coding agents classify task risk, protect research data, avoid unsafe cleanup commands, and require file-backed evidence before writing quantitative claims.

## What It Protects Against

- accidental recursive deletion or sync-delete
- cross-shell destructive commands such as `cmd /c`, `bash -c`, or SSH heredocs
- quiet/force deletion flags that hide failure signals
- overwriting frozen results or model artifacts
- manuscript numbers that cannot be traced to local evidence files
- accidental upload of private, confidential, or machine-local files

## Quick Start

Copy the skill folder into your project:

```text
.claude/skills/research-guardrails/
```

Then ask your agent:

```text
Use $research-guardrails. First classify this task as text-only, plotting-only, postprocessing-only, experiment-changing, or destructive-risk, then proceed according to the rules.
```

In Claude Code, direct invocation is also:

```text
/research-guardrails
```

If your agent does not support skills, ask it to read:

```text
.claude/skills/research-guardrails/SKILL.md
```

## Optional Setup

The skill is safe by default. It treats common research folders such as `data/`, `results/`, `models/`, `checkpoints/`, `figures/`, and `manuscript/` as protected.

For a lightweight project profile, run:

```bash
cd .claude/skills/research-guardrails
python scripts/init_project_profile.py
```

The setup asks only three questions:

1. Which directories contain irreplaceable data?
2. Which result directory or file is currently authoritative?
3. Which private/confidential paths must never be uploaded?

## Command Safety Checker

Before deletion, cleanup, overwrite, or sync-delete:

```bash
python .claude/skills/research-guardrails/scripts/check_command_safety.py '<command>'
```

If it prints `BLOCK`, do not run the command. Use dry-run output, absolute paths, and move-to-quarantine instead of permanent deletion.

## Compatibility

- Claude Code: use as a project skill via `/research-guardrails`.
- Codex: use `Use $research-guardrails`, or reference the same `SKILL.md` from `AGENTS.md` or project instructions.
- Other agents: paste the quick-start prompt and point the agent at `SKILL.md`.

See [README.zh.md](README.zh.md) for Chinese usage notes.
