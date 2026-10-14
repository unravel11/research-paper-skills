#!/usr/bin/env bash
# Install the skills in .claude/skills into ~/.claude/skills and ~/.codex/skills.
# Default: symlink. --copy: copy instead. --force: replace an existing symlink
# (a real directory with the same name is never touched). Otherwise existing
# entries are skipped. Dangling symlinks into this repository are pruned.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
mode="link"
force=0
for arg in "$@"; do
  case "$arg" in
    --copy) mode="copy" ;;
    --force) force=1 ;;
    -h|--help) sed -n '2,5p' "$0"; exit 0 ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done
for dest in "$HOME/.claude/skills" "$HOME/.codex/skills"; do
  mkdir -p "$dest"
  for src in "$here"/.claude/skills/*/; do
    name="$(basename "$src")"
    target="$dest/$name"
    if [[ -L "$target" ]]; then
      if [[ "$force" == 1 ]]; then
        rm "$target"
      else
        echo "skip  $target (symlink exists; use --force to replace)"
        continue
      fi
    elif [[ -e "$target" ]]; then
      echo "skip  $target (directory exists)"
      continue
    fi
    if [[ "$mode" == "copy" ]]; then
      cp -R "$src" "$target"
    else
      ln -s "${src%/}" "$target"
    fi
    echo "$mode  $target"
  done
  # Remove symlinks that point into this repository but whose target no longer
  # exists (a skill that was removed or merged), so stale entries do not linger.
  for link in "$dest"/*; do
    [[ -L "$link" ]] || continue
    target_path="$(readlink "$link")"
    if [[ "$target_path" == "$here/.claude/skills/"* && ! -e "$link" ]]; then
      rm "$link"
      echo "prune $link (target removed)"
    fi
  done
done
