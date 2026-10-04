# Knowledge Navigation

This file is the mandatory entry point for durable project knowledge. Keep it
short and link to project-specific domains as they are added.

## Domains

No project domains yet. Add a domain here when you start maintaining project knowledge.

## Shared resources

- [`_template/`](_template/) — copyable topic templates.
- [`_example/`](_example/) — fictional examples; never treat them as facts.
- [`log.md`](log.md) — concise record of durable knowledge changes; read when
  history, contradictions, prior decisions, or lint context matter.

## Navigation rule

Resolve the project domain first, read its index, then read only relevant topic
pages under `self/`, `derived/`, or `sources/`. `_example/`, `_template/`, and any
illustrative `domain/` folder are non-authoritative. Create real project domains
directly under `knowledge/`. Keep temporary task state outside this directory.

### Task-domain gate

Resolve the domain from the user's explicit project, business workflow, and
established conversation context. Do not infer a domain from broad keywords or
a folder name alone, or ask the user to repeat scope that context already
establishes.

Ask for the project domain only when a material ambiguity remains. If it stays
unresolved, retain supplied files unchanged under `knowledge/inbox/sources/`
and defer derived knowledge until triage. Preserve supported project details
when only one field, label, or rule remains uncertain, and record that
uncertainty with its evidence.

Select evidence by direct scope and provenance. File inventories and pages
marked `content_read: false` are navigation hints, not evidence of fields,
schemas, workflows, or business rules. A source supplied for the current task
takes precedence over a similarly named historical inventory. State which
exact source was inspected; distinguish direct evidence, broader context, and
navigation-only links when preparing a handoff.

## Write rule

Follow [AGENTS.md](../AGENTS.md#write-rules) and the
[knowledge-base skill](../.codex/skills/knowledge-base/SKILL.md) for automatic
capture, source-first intake, curation, and completion checks. Update an index
when navigation changes, log actual durable changes, and run a knowledge linter
when one is available.
