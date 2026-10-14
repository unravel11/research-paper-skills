#!/usr/bin/env python3
"""Validate the skills in .claude/skills and the repository-level docs.

Per skill directory: SKILL.md exists with frontmatter whose ``name`` equals the
directory name and whose ``description`` is non-empty; every relative markdown
link in the skill's .md files resolves to an existing file; evals/evals.json
parses when present. Repository-wide: relative links in the root .md files
resolve, and no text file contains a private absolute path (/Users/<x>,
/home/<x>, /Volumes/...).

Usage:
    python3 scripts/validate_skills.py [--skills-dir .claude/skills]

Exit 1 on any error. Warnings are printed but do not fail the run.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
PRIVATE_RE = re.compile(r"(/Users/[A-Za-z0-9_.-]+|/home/[A-Za-z0-9_.-]+|/Volumes/[A-Za-z0-9_.-]+)")
# Upstream skills kept verbatim (see THIRD_PARTY_NOTICES.md): a path-like string in their own
# test fixtures is theirs, so it is reported as a warning, not an error.
THIRD_PARTY = {
    "scientific-visualization",
    "publication-chart-skill",
    "drawio-skill",
    "academic-humanizer",
    "task-forest",
    "session-handoff-prompt",
}
TEXT_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json", ".sh", ".txt", ".csv", ".mplstyle"}
SKIP_SCHEMES = ("http://", "https://", "mailto:", "file:")


def parse_frontmatter(text: str) -> dict[str, str] | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    fields: dict[str, str] = {}
    current: str | None = None
    folded = False
    for line in lines[1:]:
        if line.strip() == "---":
            break
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if match and not line.startswith((" ", "\t")):
            current, value = match.group(1), match.group(2).strip()
            folded = value in {">", ">-", "|", "|-"}
            fields[current] = "" if folded else value.strip('"').strip("'")
        elif current and folded and line.startswith((" ", "\t")):
            fields[current] = (fields[current] + " " + line.strip()).strip()
    return fields


def check_links(md: Path, errors: list[str]) -> None:
    text = md.read_text(encoding="utf-8", errors="replace")
    for match in LINK_RE.finditer(text):
        target = match.group(1)
        if target.startswith(SKIP_SCHEMES) or target.startswith("#"):
            continue
        if "<" in target or ">" in target or "{" in target:
            continue  # placeholder such as <skill_dir>/scripts/x.py
        path = target.split("#", 1)[0]
        if not path:
            continue
        resolved = (md.parent / path).resolve()
        if not resolved.exists():
            errors.append(f"{md}: broken link -> {target}")


def scan_private_paths(path: Path, errors: list[str], warnings: list[str]) -> None:
    if path.name == "validate_skills.py":
        return
    third_party = any(part in THIRD_PARTY for part in path.parts)
    text = path.read_text(encoding="utf-8", errors="replace")
    for number, line in enumerate(text.splitlines(), 1):
        if "re.compile" in line or "PRIVATE_PATH" in line:
            continue
        match = PRIVATE_RE.search(line)
        if match:
            if third_party:
                warnings.append(f"{path}:{number}: path-like string in upstream skill ({match.group(1)}), left as is")
            else:
                errors.append(f"{path}:{number}: private path {match.group(1)}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--skills-dir", default=".claude/skills")
    args = parser.parse_args(argv)

    repo = Path(__file__).resolve().parent.parent
    skills_dir = (repo / args.skills_dir).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    skills = sorted(p for p in skills_dir.iterdir() if p.is_dir()) if skills_dir.is_dir() else []
    if not skills:
        errors.append(f"no skill directories under {skills_dir}")

    for skill in skills:
        skill_md = skill / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"{skill.name}: SKILL.md missing")
            continue
        fields = parse_frontmatter(skill_md.read_text(encoding="utf-8", errors="replace"))
        if fields is None:
            errors.append(f"{skill.name}: SKILL.md has no frontmatter")
        else:
            if fields.get("name") != skill.name:
                errors.append(f"{skill.name}: frontmatter name is {fields.get('name')!r}")
            if not fields.get("description"):
                errors.append(f"{skill.name}: frontmatter description is empty")
        for md in skill.rglob("*.md"):
            check_links(md, errors)
        evals = skill / "evals" / "evals.json"
        if evals.is_file():
            try:
                data = json.loads(evals.read_text(encoding="utf-8"))
                if not isinstance(data.get("evals"), list) or not data["evals"]:
                    errors.append(f"{skill.name}: evals.json has no evals list")
            except json.JSONDecodeError as exc:
                errors.append(f"{skill.name}: evals.json invalid JSON: {exc}")
        elif skill.name not in THIRD_PARTY:
            warnings.append(f"{skill.name}: no evals/evals.json")
        if skill.name not in THIRD_PARTY and not (skill / "agents" / "openai.yaml").is_file():
            warnings.append(f"{skill.name}: no agents/openai.yaml (Codex interface metadata)")

    for md in repo.glob("*.md"):
        check_links(md, errors)
    for md in (repo / "docs").glob("*.md") if (repo / "docs").is_dir() else []:
        check_links(md, errors)

    for path in repo.rglob("*"):
        if ".git" in path.parts or not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        scan_private_paths(path, errors, warnings)

    for warning in warnings:
        print(f"warning: {warning}")
    for error in errors:
        print(f"error: {error}")
    print(f"{len(skills)} skills checked; {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
