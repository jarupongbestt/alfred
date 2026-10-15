# Scripts

Put shared setup scripts here. Add project-specific scripts under a named subfolder and document their entry points here.

- `setup-skills-links.ps1` — creates Windows junctions from `.agents/skills` and `.claude/skills` to `.codex/skills`.
- `knowledge/check.sh` — runs the read-only knowledge checks from any working directory; use `sh scripts/knowledge/check.sh`. Requires Python 3.10+; `KNOWLEDGE_PYTHON` may select an existing interpreter. No installation or credentials.
- `knowledge/validate_knowledge.py` — pinned upstream standard-library checker; see [validation](../knowledge/_system/validation.md) and [adoption provenance](../knowledge/_system/adoption.md).
