#!/usr/bin/env python3
"""Shared per-skill validator for blaze-craft.

Usage: python3 validate_skill.py <skill_dir>

Validates:
- SKILL.md exists
- SKILL.md has YAML frontmatter with `name` and `description`
- references/ contains all 5 expected files
- scripts/validate_skill.py exists (the thin wrapper)
"""
from __future__ import annotations

import sys
from pathlib import Path

EXPECTED_REFS = {
    "workflow-playbook.md",
    "anti-patterns.md",
    "quality-rubric.md",
    "examples.md",
    "official-sources.md",
}


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def validate(skill_dir: Path) -> None:
    if not skill_dir.is_dir():
        fail(f"skill dir does not exist: {skill_dir}")

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        fail(f"SKILL.md missing in {skill_dir}")

    # Parse frontmatter without YAML lib (keep stdlib only).
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"SKILL.md missing YAML frontmatter opening fence in {skill_dir}")

    end = text.find("\n---\n", 4)
    if end == -1:
        fail(f"SKILL.md missing YAML frontmatter closing fence in {skill_dir}")

    frontmatter = text[4:end]
    has_name = False
    has_description = False
    for line in frontmatter.splitlines():
        stripped = line.strip()
        if stripped.startswith("name:"):
            has_name = True
        if stripped.startswith("description:"):
            has_description = True

    if not has_name:
        fail(f"SKILL.md frontmatter missing `name` field in {skill_dir}")
    if not has_description:
        fail(f"SKILL.md frontmatter missing `description` field in {skill_dir}")

    refs_dir = skill_dir / "references"
    if not refs_dir.is_dir():
        fail(f"references/ missing in {skill_dir}")

    found_refs = {p.name for p in refs_dir.iterdir() if p.is_file()}
    missing = EXPECTED_REFS - found_refs
    if missing:
        fail(f"references/ missing files in {skill_dir}: {sorted(missing)}")

    wrapper = skill_dir / "scripts" / "validate_skill.py"
    if not wrapper.is_file():
        fail(f"scripts/validate_skill.py wrapper missing in {skill_dir}")

    print(f"OK: {skill_dir.name} skill scaffold valid")


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: validate_skill.py <skill_dir>", file=sys.stderr)
        sys.exit(2)

    validate(Path(sys.argv[1]).resolve())


if __name__ == "__main__":
    main()
