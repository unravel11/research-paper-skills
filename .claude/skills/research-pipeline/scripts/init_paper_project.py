#!/usr/bin/env python3
"""Create the research-pipeline project skeleton inside a paper repository.

Copies ``assets/project-skeleton/`` into PROJECT_DIR, fills the
``{{PAPER_ID}}``, ``{{VENUE}}``, ``{{DATE}}`` and ``{{ACTOR}}`` placeholders,
and never overwrites: a file that already exists is reported and left alone,
so the script is safe to re-run on a project that already has some of the
files. It creates no git commit and runs no other skill.

``--state-only`` writes just ``research/STATE.md`` and ``PROGRESS.md``. Use it
for a project that already has its own file layout: do not rename or move its
files; list their real paths in STATE.md's ``阶段产出索引`` as
``默认路径 → 实际路径`` and ``check_gates.py`` follows the index.

Usage:
    python3 init_paper_project.py PROJECT_DIR [--paper-id ID] [--venue NAME]
                                  [--actor NAME] [--state-only] [--dry-run]
"""

from __future__ import annotations

import argparse
import datetime as _dt
import sys
from pathlib import Path

SKELETON = Path(__file__).resolve().parent.parent / "assets" / "project-skeleton"
PLACEHOLDERS = ("PAPER_ID", "VENUE", "DATE", "ACTOR")
STATE_ONLY = ("research/STATE.md", "PROGRESS.md")


def fill(text: str, values: dict[str, str]) -> str:
    for key in PLACEHOLDERS:
        text = text.replace("{{" + key + "}}", values[key])
    return text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project_dir", help="paper project root (created if missing)")
    parser.add_argument("--paper-id", default=None, help="paper ID written into research/STATE.md (default: directory name)")
    parser.add_argument("--venue", default="UNDECIDED", help="target venue or UNDECIDED (default)")
    parser.add_argument("--actor", default="Claude", help="who performs the initial check (Claude / Codex / name)")
    parser.add_argument("--state-only", action="store_true", help="create only research/STATE.md and PROGRESS.md (project already has its own layout)")
    parser.add_argument("--dry-run", action="store_true", help="report what would be created without writing")
    args = parser.parse_args(argv)

    if not SKELETON.is_dir():
        print(f"error: skeleton directory not found: {SKELETON}", file=sys.stderr)
        return 2

    root = Path(args.project_dir).expanduser().resolve()
    values = {
        "PAPER_ID": args.paper_id or root.name,
        "VENUE": args.venue,
        "DATE": _dt.date.today().isoformat(),
        "ACTOR": args.actor,
    }

    created: list[str] = []
    skipped: list[str] = []
    for src in sorted(p for p in SKELETON.rglob("*") if p.is_file()):
        rel = src.relative_to(SKELETON)
        if args.state_only and rel.as_posix() not in STATE_ONLY:
            continue
        dst = root / rel
        if dst.exists():
            skipped.append(rel.as_posix())
            continue
        data = src.read_bytes()
        try:
            data = fill(data.decode("utf-8"), values).encode("utf-8")
        except UnicodeDecodeError:
            pass
        if not args.dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(data)
        created.append(rel.as_posix())

    verb = "would create" if args.dry_run else "created"
    print(f"project: {root}")
    print(f"paper ID: {values['PAPER_ID']}   venue: {values['VENUE']}   date: {values['DATE']}")
    for rel in created:
        print(f"  {verb}  {rel}")
    for rel in skipped:
        print(f"  skipped  {rel} (exists)")
    print()
    print("下一步：调用 $research-pipeline 判定阶段。新项目从 R0 开始，先由你自己输入 /innovation-explore 确定研究设定（它只能由用户触发）。")
    print("已有材料的项目不必搬文件：在 research/STATE.md 的阶段产出索引里写“默认路径 → 实际路径”，")
    print("把当前阶段改成产物实际到达的阶段，再运行 check_gates.py；它按索引找文件。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
