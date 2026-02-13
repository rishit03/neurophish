#!/usr/bin/env python3
"""
migrate_score_calls.py

Finds patterns like:
    label, reason = scorer.score(<args>)

and replaces them with a safe unpack:

    out = scorer.score(<args>)
    label, reason = out[0], out[1]
    meta = out[2] if isinstance(out, (list, tuple)) and len(out) > 2 else None

Backs up each modified file to <filename>.bak and prints a report.
Ignores lines that are commented out (leading # after indentation).
Excludes node_modules, .git, and typical venv dirs.

Notes:
- This script is conservative: it only replaces single-line scorer.score(...) calls.
- Multiline calls or unusual formatting will be skipped (safer).
"""
import re
import sys
from pathlib import Path
from typing import List

ROOT = Path(".").resolve()
EXCLUDE_DIRS = {"node_modules", ".git", "__pycache__", ".venv", "venv", ".mypy_cache", "env", "ENV"}

# Regex to find lines like:
#    label, reason = scorer.score(some, args)
# Captures indentation and the call args.
# This intentionally only matches single-line calls.
PAT = re.compile(r'^(\s*)(?P<line>label\s*,\s*reason\s*=\s*scorer\.score\((?P<args>.*)\)\s*)(#.*)?$')

def should_exclude(path: Path) -> bool:
    """
    Return True if the path is inside an excluded directory.
    """
    parts = set(path.resolve().parts)  # parts are strings of path components
    return bool(parts & EXCLUDE_DIRS)

def find_python_files(root: Path) -> List[Path]:
    files = []
    for p in root.rglob("*.py"):
        # skip files inside excluded directories
        if should_exclude(p):
            continue
        # skip this script itself
        if p.resolve() == Path(__file__).resolve():
            continue
        files.append(p)
    return files

def process_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines(keepends=True)
    changed = False
    new_lines = []
    for i, line in enumerate(lines):
        m = PAT.match(line)
        if not m:
            new_lines.append(line)
            continue
        indent = m.group(1) or ""
        args = m.group("args").strip()
        # safety: skip if probable multiline (unbalanced parens) or extremely long args
        if args.count("(") != args.count(")") or len(args) > 1000:
            new_lines.append(line)
            print(f"[SKIP-MULTILINE] {path}:{i+1} (multiline or complex args) -- manual fix recommended")
            continue

        # Build replacement block
        repl = (
            f"{indent}out = scorer.score({args})\n"
            f"{indent}label, reason = out[0], out[1]\n"
            f"{indent}meta = out[2] if isinstance(out, (list, tuple)) and len(out) > 2 else None\n"
        )
        new_lines.append(repl)
        changed = True
        print(f"[PATCH] {path}:{i+1}  -- replaced 'label, reason = scorer.score(...)'")

    if changed:
        # create backup (don't overwrite existing backup)
        bak = path.with_suffix(path.suffix + ".bak")
        if not bak.exists():
            path.rename(bak)
            bak.write_text("".join(lines), encoding="utf-8", errors="ignore")
            path.write_text("".join(new_lines), encoding="utf-8")
        else:
            # create numbered backup
            idx = 1
            while True:
                bak2 = path.with_suffix(path.suffix + f".bak{idx}")
                if not bak2.exists():
                    path.rename(bak2)
                    bak2.write_text("".join(lines), encoding="utf-8", errors="ignore")
                    path.write_text("".join(new_lines), encoding="utf-8")
                    break
                idx += 1
    return 1 if changed else 0

def main():
    print(f"Scanning Python files under {ROOT} (this may take a moment)...")
    py_files = find_python_files(ROOT)
    total = 0
    modified_files = []
    for f in py_files:
        # quick pre-check to avoid opening files unnecessarily
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if "label, reason = scorer.score(" not in text:
            continue
        modified = process_file(f)
        if modified:
            modified_files.append(f)
            total += 1

    print(f"\nDone. Modified {total} Python file(s).")
    if modified_files:
        print("Modified files:")
        for f in modified_files:
            print(f"  - {f}")
        print("\nBackups saved with .bak suffix (or .bakN if existing). Review changes before committing.")
    else:
        print("No files needed modification.")

if __name__ == "__main__":
    main()
