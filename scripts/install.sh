#!/usr/bin/env bash
# Install the ANT engine into a target project.
# Usage: scripts/install.sh /path/to/your/project
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${1:-}"

if [ -z "$DEST" ]; then
  echo "usage: $0 /path/to/your/project" >&2
  exit 1
fi
if [ ! -d "$DEST" ]; then
  echo "error: $DEST is not a directory" >&2
  exit 1
fi

mkdir -p "$DEST/.claude/agents" "$DEST/.claude/commands"

for f in "$SRC"/agents/*.md; do
  name="$(basename "$f")"
  if [ -e "$DEST/.claude/agents/$name" ]; then
    echo "skip   .claude/agents/$name (already present)"
  else
    cp "$f" "$DEST/.claude/agents/$name"
    echo "copied .claude/agents/$name"
  fi
done

for f in "$SRC"/commands/*.md; do
  name="$(basename "$f")"
  if [ -e "$DEST/.claude/commands/$name" ]; then
    echo "skip   .claude/commands/$name (already present)"
  else
    cp "$f" "$DEST/.claude/commands/$name"
    echo "copied .claude/commands/$name"
  fi
done

for f in PROTOCOL.md COORDINATOR.md; do
  if [ -e "$DEST/$f" ]; then
    echo "skip   $f (already present)"
  else
    cp "$SRC/$f" "$DEST/$f"
    echo "copied $f"
  fi
done

echo
echo "Next: cd $DEST && $SRC/scripts/bootstrap.sh"
