# Configuration

The skill is safe by default and does not require setup. Use configuration only when project-specific paths matter.

## Recommended Defaults

This section is the source of truth for the default protected/private path lists used in README files, tutorials, and setup examples.

If no `project-profile.yaml` exists, assume:

- protected paths: `data/`, `datasets/`, `raw/`, `results/`, `outputs/`, `models/`, `checkpoints/`, `figures/`, `manuscript/`, `paper/`
- private paths: `.env`, `.ssh/`, `secrets/`, `private/`, `confidential/`
- deletion behavior: move to quarantine, not permanent deletion
- evidence behavior: every number in a manuscript/report must point to a local file

## Three-Question Setup

Ask the user only:

1. Which directories contain irreplaceable data?
2. Which result directory or file is currently authoritative?
3. Which private/confidential paths must never be uploaded?

Do not ask for exhaustive schemas, every metric, or every experiment. The profile can be refined later.

## Interactive Setup

From the skill directory:

```bash
python scripts/init_project_profile.py
```

This writes `project-profile.yaml` in the current directory. Review it before committing or sharing.

## Agent Behavior

If `project-profile.yaml` exists, read it before destructive operations, publication claims, or GitHub release work. If it does not exist, proceed with defaults and ask the three setup questions only when the missing information affects safety.
