#!/bin/sh
# Read-only entry point for the pinned knowledge validator. No credentials needed.
set -eu
knowledge_repo=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
knowledge_python=${KNOWLEDGE_PYTHON:-}
if [ -z "$knowledge_python" ]; then
  for knowledge_candidate in python3.13 python3.12 python3.11 python3.10 python3 "$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"; do
    if "$knowledge_candidate" -B -S -c 'import sys; sys.exit(sys.version_info < (3, 10))' >/dev/null 2>&1; then
      knowledge_python=$knowledge_candidate
      break
    fi
  done
fi
if [ -z "$knowledge_python" ] || ! "$knowledge_python" -B -S -c 'import sys; sys.exit(sys.version_info < (3, 10))' >/dev/null 2>&1; then
  echo 'Knowledge validation requires Python 3.10+; set KNOWLEDGE_PYTHON to a compatible interpreter.' >&2
  exit 2
fi
exec "$knowledge_python" -B -S "$knowledge_repo/scripts/knowledge/validate_knowledge.py" \
  --repo-root "$knowledge_repo" --knowledge-root "$knowledge_repo/knowledge" \
  --layout "$knowledge_repo/knowledge/validation-layout.yaml"
