#!/usr/bin/env bash
# Create the empty ledgers the agents expect, in the CURRENT project.
# Run this BEFORE the first pass: the agents are instructed to edit files that already
# exist, because some harnesses refuse to create new report-shaped files.
# Usage: cd /path/to/your/project && /path/to/descartes/scripts/bootstrap.sh
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$(pwd)"

if [ "$SRC" = "$DEST" ]; then
  echo "error: run this from inside your own project, not from the engine repo" >&2
  exit 1
fi

created=0
skipped=0

while IFS= read -r rel; do
  target="$DEST/.claude/agent-memory/$rel"
  mkdir -p "$(dirname "$target")"
  if [ -e "$target" ]; then
    echo "skip    .claude/agent-memory/$rel"
    skipped=$((skipped + 1))
  else
    cp "$SRC/templates/agent-memory/$rel" "$target"
    echo "created .claude/agent-memory/$rel"
    created=$((created + 1))
  fi
done < <(cd "$SRC/templates/agent-memory" && find . -name '*.md' | sed 's|^\./||' | sort)

echo
echo "$created created, $skipped already present."
echo "Pre-register your first ant in .claude/agent-memory/data-reuse-discovery-ant/ANT_REGISTRY.md"
echo "BEFORE touching any data, then fire the first pass."
