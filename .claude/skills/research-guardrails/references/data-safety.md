# Data Safety Guardrails

Use this reference for cleanup, deletion, remote server work, backup, Git operations, or anything that can remove or overwrite data.

## Red Lines

- No recursive deletion by default: block `rm -rf`, `find ... -exec rm`, `find ... -delete`, `rsync --delete`, `trash`/`gio trash` on directories, `Remove-Item -Recurse`, `rd /s`, and bulk `mv` over existing targets until audited.
- No cross-shell destructive execution: block `cmd /c`, `powershell -Command`, `bash -c`, SSH heredocs, or generated scripts when they contain delete/move/overwrite operations. Cross-shell quoting changes the command semantics.
- No quiet/ignore-error destructive execution: block `/q`, `-Force`, `-ErrorAction SilentlyContinue`, `2>/dev/null`, or equivalent suppression when combined with delete/move/overwrite operations.
- If a destructive cleanup fails once because of locks, permissions, path errors, or “resource busy”, stop. Do not switch shells, add force/quiet flags, background the job, or bypass the lock without a new exact-command review.
- No destructive command may depend on an unset variable, relative path, glob expansion, or inherited current working directory.
- No cleanup in canonical paths unless the user explicitly authorizes the exact path and backup state.
- No deletion of raw source data, model checkpoints, scalers, split files, source-data workbooks, posterior samples, VTU fields, or manuscript source figures.
- No `git add -A`; stage exact paths only.
- Do not upload confidential directories, credentials, `.ssh`, tokens, private machine config, or accidental large personal files.

## Mandatory Shell Patterns

For any destructive shell script:

```bash
set -euo pipefail
TARGET="/absolute/path"
: "${TARGET:?TARGET is empty}"
test -d "$TARGET"
case "$TARGET" in
  /absolute/project/path/*|/absolute/quarantine/path/*) ;;
  *) echo "Refusing unexpected target: $TARGET" >&2; exit 2 ;;
esac
find "$TARGET" -maxdepth 1 -mindepth 1 -type d -mmin +60 -print
```

Only after the printed list is reviewed may a destructive replacement be considered. Prefer:

```bash
mkdir -p /absolute/quarantine
mv "$TARGET/specific_item" /absolute/quarantine/
```

over permanent deletion.

Before any destructive command, show the final resolved semantics:

- shell type and working directory
- absolute target path after variable expansion
- dry-run list of affected files/directories
- backup or pushed Git remote that can restore the target
- exact command to run, with no hidden wrapper such as `cmd /c`

## Remote Server Rules

- Before running cleanup on a server, record `pwd`, `hostname`, `df -h`, and the exact absolute target path.
- Never generate a remote cleanup script with uninspected heredoc variable interpolation. If a script is generated, `cat` it back and inspect it before execution.
- Never background a destructive job until its dry-run output has been captured.
- If SSH fails after cleanup, do not keep guessing. Ask for physical-console verification because `.ssh/authorized_keys` or home-directory files may be gone.

## Generated Script Review

Deletion can hide inside helper scripts. Treat the following as destructive even if the outer command is just `python`, `node`, `bash`, or `powershell`:

- Python: `shutil.rmtree`, `os.remove`, `Path.unlink`, `Path.rmdir`, loops over `glob` followed by delete
- Node.js: `fs.rm(... recursive: true)`, `fs.rmdir`, `fs.unlink`
- Shell/batch: `rm -r`, `rm -rf`, `find -delete`, `rd /s`, `rmdir /s`, `del /s`, `git clean -fdx`
- PowerShell: `Remove-Item -Recurse`, `Get-ChildItem -Recurse | Remove-Item`

For generated scripts, first print the resolved deletion target list, then require a second confirmation. The default replacement is move-to-quarantine; the agent must not empty quarantine.

## Backup Rules

- Before deleting or replacing any valuable directory, verify at least one independent copy exists.
- Irreplaceable research assets should have at least local + GitHub or local + external disk; raw source/HF data should have a third cold copy when feasible.
- Commit is not backup until pushed. Always verify with `git status --short` and `git log --oneline origin/<branch>..HEAD`.

## Git Rules

Safe sequence:

```bash
git status --short
git add path/to/known-file path/to/known-dir
git diff --cached --stat
git diff --cached --name-only
git commit -m "..."
git push
git status --short
```

Before sharing or moving project files, list local-only data-like files:

```bash
git status --short --untracked-files=all | rg '\.(csv|json|npz|npy|pt|pth|pkl|h5|vtu|xlsx|tex|md|py)$'
```
