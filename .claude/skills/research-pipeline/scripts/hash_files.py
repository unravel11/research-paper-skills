#!/usr/bin/env python3
"""Print SHA-256 hashes as the markdown table used by the R2 protocol.

The protocol's 运行与冻结 section records every training, evaluation and
analysis script as ``| path | sha256 |`` rows. ``check_gates.py`` re-reads
rows of that shape and compares them with the working tree, so paths are
printed relative to ``--base`` (default: the current directory, which should
be the project root).

Usage:
    python3 hash_files.py [--base DIR] PATH_OR_GLOB ...
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import os
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="+", help="files or globs (** allowed)")
    parser.add_argument("--base", default=".", help="directory the printed paths are relative to (project root)")
    args = parser.parse_args(argv)

    base = Path(args.base).resolve()
    files: list[Path] = []
    for pattern in args.paths:
        matches = sorted(glob.glob(pattern, recursive=True))
        if not matches and Path(pattern).exists():
            matches = [pattern]
        for match in matches:
            path = Path(match)
            if path.is_file() and path not in files:
                files.append(path)
    if not files:
        print("error: no files matched", file=sys.stderr)
        return 2

    print("| 路径 | SHA-256 |")
    print("|---|---|")
    for path in files:
        try:
            rel = Path(os.path.relpath(path.resolve(), base)).as_posix()
        except ValueError:
            rel = path.as_posix()
        print(f"| `{rel}` | {sha256(path)} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
