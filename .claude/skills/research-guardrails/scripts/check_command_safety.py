#!/usr/bin/env python3
"""Conservative command safety checker for cleanup/destructive operations."""

from __future__ import annotations

import re
import shlex
import sys


BLOCK_PATTERNS = [
    (r"\brm\s+[^;\n]*-[^\s]*r[^\s]*f|rm\s+[^;\n]*-[^\s]*f[^\s]*r", "recursive force delete"),
    (r"\bfind\b[^;\n]*(?:-delete|-exec\s+rm\b)", "find deletes files"),
    (r"\brsync\b[^;\n]*--delete", "rsync delete"),
    (r"\bRemove-Item\b[^;\n]*-Recurse", "PowerShell recursive delete"),
    (r"\bGet-ChildItem\b[^;\n]*-Recurse[^;\n]*\|\s*Remove-Item\b", "PowerShell recursive traversal piped to delete"),
    (r"\brd\s+/s\b|\brmdir\s+/s\b", "Windows recursive directory delete"),
    (r"\bdel\s+/s\b", "Windows recursive file delete"),
    (r"\bcmd\s*/c\b[^;\n]*(?:\brd\b|\brmdir\b|\bdel\b)[^;\n]*(?:/s|/q)", "cmd.exe wrapper around quiet/recursive delete"),
    (r"\bgit\s+clean\b[^;\n]*-[^\s]*f[^\s]*d[^\s]*x", "git clean removes untracked files recursively"),
    (r"\bshutil\.rmtree\b|\bos\.remove\b|\bPath\.(?:unlink|rmdir)\b", "Python script contains delete API"),
    (r"\bfs\.(?:rm|rmdir|unlink)\b", "Node script contains delete API"),
    (r"\bsudo\s+rm\b", "sudo delete"),
    (r"\bchmod\s+-R\b|\bchown\s+-R\b", "recursive permission/owner change"),
]

WARN_PATTERNS = [
    (r"\$[A-Za-z_][A-Za-z0-9_]*", "contains shell variable; require ${VAR:?} assertion for destructive use"),
    (r"\s\.\s|\s\./|\s\*", "contains relative path or glob; require explicit audit"),
    (r"<<\s*EOF|<<\s*[A-Z]+", "heredoc script generation; cat generated script before running"),
    (r"\bnohup\b|\bsetsid\b|&\s*$", "background job; require reviewed dry-run output first"),
    (r"\b(?:cmd|powershell|pwsh|bash|sh)\s+(?:/c|-Command|-c)\b", "cross-shell wrapper; require final resolved semantics"),
    (r"(?:/q\b|-Force\b|-ErrorAction\s+SilentlyContinue|2>\s*/dev/null)", "quiet/force/error-suppression flag; unsafe in destructive context"),
]

SAFE_REQUIRED_FOR_DESTRUCTIVE = [
    "set -euo pipefail",
    ": \"${",
]


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: check_command_safety.py '<command>'", file=sys.stderr)
        return 2

    command = " ".join(sys.argv[1:])
    findings: list[tuple[str, str]] = []

    for pattern, reason in BLOCK_PATTERNS:
        if re.search(pattern, command, flags=re.IGNORECASE | re.DOTALL):
            findings.append(("BLOCK", reason))

    for pattern, reason in WARN_PATTERNS:
        if re.search(pattern, command, flags=re.IGNORECASE | re.DOTALL):
            findings.append(("WARN", reason))

    destructive = any(level == "BLOCK" for level, _ in findings)
    if destructive and not all(req in command for req in SAFE_REQUIRED_FOR_DESTRUCTIVE):
        findings.append(("BLOCK", "destructive command lacks set -euo pipefail and non-empty variable assertion"))

    try:
        tokens = shlex.split(command)
    except ValueError:
        tokens = []
        findings.append(("WARN", "command could not be parsed by shlex"))

    if tokens:
        risky_roots = {"/", "/home", "/Users", "/Volumes", "C:\\", "D:\\"}
        for tok in tokens:
            if tok in risky_roots:
                findings.append(("BLOCK", f"target is broad root-like path: {tok}"))

    if findings:
        max_level = "BLOCK" if any(level == "BLOCK" for level, _ in findings) else "WARN"
        print(max_level)
        for level, reason in findings:
            print(f"- {level}: {reason}")
        return 1 if max_level == "BLOCK" else 0

    print("PASS")
    print("- No high-risk pattern detected. This is not approval; still perform path, dry-run, and backup checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
