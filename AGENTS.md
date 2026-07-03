# Agent Instructions

Before any research data, result, manuscript, recovery, cleanup, deletion, overwrite, sync, or GitHub publishing task, read:

```text
.claude/skills/research-guardrails/SKILL.md
```

Classify the task as `text-only`, `plotting-only`, `postprocessing-only`, `experiment-changing`, or `destructive-risk` before acting.

For destructive-risk tasks, run the bundled command checker and stop on `BLOCK`.

For manuscript or report claims, bind every quantitative claim to a local evidence file or mark it as pending audit.
