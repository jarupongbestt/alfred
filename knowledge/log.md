# Knowledge Change Log

Record actual durable knowledge changes concisely, with links to affected pages.
Do not store conversation transcripts or routine no-change decisions. Add actual entries using the
[action-log contract](_system/contracts.md#action-log).

## Entries

```yaml
- timestamp: "2026-10-15T03:21:53Z"
  action: reconcile
  summary: "Recheck knowledge-management adoption against fresh GitHub HEAD a05a718 (v0.3.0) and retain unchanged source evidence. Preserve required upstream method clauses; add actionable frontmatter/source_refs authoring, direct template routes and accurate native log/layout labels. Document command-only topic provenance versus structured evidence and preserve substantive claim review beyond checker success."
  paths:
    - .codex/skills/knowledge-base/SKILL.md
    - knowledge/_system/adoption.md
    - knowledge/_system/validation.md
    - knowledge/_system/evidence/2026-10-15-source-audit.json
    - knowledge/_system/evidence/2026-10-15-source-audit-preflight.json
    - knowledge/log.md
    - knowledge/inbox/sources/agent-harness-concept-2026-10-15-audit/head.json
    - knowledge/inbox/sources/agent-harness-concept-2026-10-15-audit/upstream-a05a718.tar.gz
    - knowledge/inbox/sources/agent-harness-concept-2026-10-15-audit/manifest.json
    - .gitignore
  evidence:
    - kind: artifact
      target: inbox/sources/agent-harness-concept-2026-10-15-audit/manifest.json
    - kind: artifact
      target: _system/evidence/2026-10-15-source-audit.json
  checks:
    - status: passed
      reason: "Preflight source-clause parity, 22 retained source files, four templates, unchanged validator, skill validation, authoring examples and native links passed. Final integrity validation follows this log entry and is reported separately in the task outcome."
      command: sh scripts/knowledge/check.sh
      evidence:
        - kind: artifact
          target: _system/evidence/2026-10-15-source-audit-preflight.json
- timestamp: "2026-10-15T03:03:51Z"
  action: update
  summary: "Move assistant operating references from docs to knowledge/_system. Reserve docs for project concepts, PRDs and deliverable documentation; update native navigation, metadata, references and classifications. Preserve historical report bytes and translate live historical log paths to their relocated targets."
  paths:
    - AGENTS.md
    - README.md
    - docs/README.md
    - .codex/skills/knowledge-base/SKILL.md
    - .codex/skills/documentation-and-adrs/SKILL.md
    - scripts/README.md
    - knowledge/main.md
    - knowledge/log.md
    - knowledge/validation-layout.yaml
    - knowledge/_system/index.md
    - knowledge/_system/getting-started.md
    - knowledge/_system/adoption.md
    - knowledge/_system/contracts.md
    - knowledge/_system/validation.md
    - knowledge/_system/evidence/docs-layout-preflight.json
    - .gitignore
  evidence:
    - kind: local
      target: ../AGENTS.md#document-placement
  checks:
    - status: passed
      reason: "Preflight knowledge validation and native links passed; retained reports and pinned upstream hashes match. Final validation runs after this log entry and is reported separately in the task outcome."
      command: sh scripts/knowledge/check.sh
      evidence:
        - kind: artifact
          target: _system/evidence/docs-layout-preflight.json
```
