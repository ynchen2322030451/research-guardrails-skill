# Agent Instructions

Before any research data, result, recovery, cleanup, deletion, overwrite, sync, or server task, read:

```text
.claude/skills/research-guardrails/SKILL.md
```

Classify the task as `text-only`, `plotting-only`, `postprocessing-only`, `experiment-changing`, or `destructive-risk` before acting.

For destructive-risk tasks, run the bundled command checker and stop on `BLOCK`.
