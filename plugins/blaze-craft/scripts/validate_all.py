#!/usr/bin/env python3
"""Walk every skill in skills/ and run the shared validator against it.

Exits 0 if all skills pass, 1 if any fail.
"""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

PLUGIN_DIR = Path(__file__).resolve().parent.parent
SKILLS_DIR = PLUGIN_DIR / "skills"
SHARED = PLUGIN_DIR / "scripts" / "validate_skill.py"


def main() -> None:
    if not SKILLS_DIR.is_dir():
        print(f"FAIL: skills/ dir missing at {SKILLS_DIR}", file=sys.stderr)
        sys.exit(1)

    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    if not skill_dirs:
        print(f"FAIL: no skills found under {SKILLS_DIR}", file=sys.stderr)
        sys.exit(1)

    failures = 0
    for skill_dir in skill_dirs:
        try:
            sys.argv = [str(SHARED), str(skill_dir)]
            runpy.run_path(str(SHARED), run_name="__main__")
        except SystemExit as exc:
            if exc.code != 0:
                failures += 1

    print()
    if failures:
        print(f"FAIL: {failures} of {len(skill_dirs)} skill scaffolds invalid")
        sys.exit(1)
    print(f"OK: all {len(skill_dirs)} skill scaffolds valid")


if __name__ == "__main__":
    main()
