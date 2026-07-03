# Publication and Group Handoff

Use this reference when preparing a GitHub package, collaborator handoff, or lab-wide agent rules.

## Recommended Repository Layout

Keep the reusable guardrails in:

```text
.claude/skills/research-guardrails/
  SKILL.md
  project-profile.example.yaml
  agents/openai.yaml
  references/
  scripts/
```

For Codex users, the same folder can be copied into a repo and referenced in `AGENTS.md`:

```markdown
Before any research data, result, manuscript, recovery, or cleanup task, read
`.claude/skills/research-guardrails/SKILL.md` and follow it.
```

For Claude Code users, invoke:

```text
$research-guardrails
```

## Group Rules

- Keep general safety rules in `data-safety.md`.
- Keep project-specific paths and numbers in `evidence-ledger.md` or a copied project profile.
- Prefer recommended defaults. During setup, ask the user to verify only protected directories, authoritative results, and confidential upload exclusions.
- If a small setup flow is helpful, run `python .claude/skills/research-guardrails/scripts/init_project_profile.py` and review the generated `project-profile.yaml`.
- Keep incident-specific lessons in `recovery-playbook.md`.
- Do not put secrets, private data, or patented material into the skill.
- When a new result track becomes canonical, update the evidence ledger and add a dated note.

## Before Pushing to GitHub

Run:

```bash
git status --short --untracked-files=all
git diff --cached --name-only
find .claude/skills/research-guardrails -type f | sort
```

Check that no file contains:

- passwords, tokens, SSH keys
- private host credentials
- unpublished patent material
- large binary research data that should live in release storage instead of rules

## Minimal Handoff Prompt

Use this with a new agent:

```text
Use $research-guardrails. First classify the task as text-only, plotting-only,
postprocessing-only, experiment-changing, or destructive-risk. Then proceed only
after binding any scientific claim to a local evidence file.
```
