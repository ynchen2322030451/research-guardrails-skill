# Minimal Prompts

## Claude Code Skill Prompt

```text
/research-guardrails
```

## Codex Skill Prompt

```text
Use $research-guardrails. First classify this task as text-only, plotting-only, postprocessing-only, experiment-changing, or destructive-risk, then proceed according to the rules.
```

## Universal Agent Prompt

```text
Please follow the research-guardrails rules. Before acting, classify the task risk. For deletion, cleanup, overwrite, sync, server work, or recovery, check paths, backups, and affected files first.
```

## Three-Question Setup Prompt

```text
Use the recommended defaults and ask me only three setup questions: which directories contain irreplaceable data, which result directory or file is authoritative, and which private/confidential paths must never be uploaded.
```
