# Research Guardrails Skill

A reusable AI-agent guardrail skill for research projects. It helps Claude Code, Codex, and other coding agents classify task risk, protect research data, and avoid unsafe cleanup or overwrite commands.

## What It Protects Against

- accidental recursive deletion or sync-delete
- cross-shell destructive commands such as `cmd /c`, `bash -c`, or SSH heredocs
- quiet/force deletion flags that hide failure signals
- overwriting frozen results or model artifacts
- accidental upload of private, confidential, or machine-local files

## Quick Start

Copy the skill folder into your project:

```text
.claude/skills/research-guardrails/
```

Or ask your AI agent:

```text
Please download the research-guardrails skill from https://github.com/ynchen2322030451/research-guardrails-skill and install it into the current project's .claude/skills/research-guardrails/. Before installing, check whether that target directory already exists; if it exists, do not overwrite it without asking me.
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

The skill is safe by default. The default protected/private path lists are maintained in `references/configuration.md`.

The bundled evidence ledger is a template; fields marked `TODO / 待填写` are placeholders to replace for your project.

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
