---
name: knowledge-base
description: Retrieve and curate evidence-backed durable knowledge using approved paths, metadata, navigation, and integrity checks.
---

# Knowledge Base

Resolve the target's approved knowledge root, startup entry, categories, protected
areas, action log, and check command from project instructions or the adapter map.
Never infer paths from this repository's example tree. Full workflow includes
knowledge management; a partial adoption without it may omit this method with an
explicit `outside_scope` reason.

## Retrieve before scanning

Main Agent, Intake, and Planner read the configured startup entry, then the
matching domain index's `## Navigation Hints`, the relevant topic, and focused
`source_refs`, before broader project searches. Use hints to constrain scope,
not as proof that a claim is true. When a page or hint is absent, stale,
contradictory, or insufficient, record the evidence and reason for a narrow
expansion. Do not preload the whole knowledge tree or invent domain indexes.
Read the action log only for history, contradictions, recurring failures, audit,
or lint context. Read raw sources only when their exact evidence is needed.

A configured domain index keeps navigation concise. Its `## Navigation Hints`
uses a Markdown table with `Task | Target` columns; each target is one local
inline link to an existing page or category. `No navigation hints yet.` is the
explicit empty state. Topic details belong in topic pages.

## Choose durable changes

Read existing relevant pages and check equivalent meaning before choosing:

- Skip duplicate, temporary, unsupported, code-obvious, or non-durable material.
- Update the existing home for corrections, evidence, or useful qualifications.
- Merge overlap while preserving distinct facts, exceptions, and evidence.
- Split mixed topics only when focused retrieval improves and links survive.
- Create a page when eligible information has no suitable existing home.

Keep decisions, constraints, procedures, and recurring failure patterns that
will help future work. Exclude task diaries, transcripts, copied code, and
unsupported claims. Preserve the target's category rules: internal discoveries
and ADRs, faithful external compilations, and protected raw inputs are distinct.
Locked derived content changes only through an explicitly approved source re-sync;
normal curation must not rewrite raw material. Reorganization stays within scope,
maintains navigation and references, and preserves provenance and exceptions.

Resolve contradictions by comparing evidence, versions, and conditions. Explain
any correction or supersession; preserve unresolved disagreements explicitly.
Do not silently prefer the newest claim.

## Topic and reference contract

Ordinary Markdown knowledge pages have YAML frontmatter with `type`,
`description`, `source_refs`, `updated`, and `status`. `type` is `self`, `derived`,
`adr`, or `source-companion`; `description` is a nonempty single line.
`updated` is an actual `YYYY-MM-DD` date. `source_refs` is a nonempty list of
`{kind: local|url|command|artifact, target: ...}` mappings. Local and artifact
references are page-relative, exist inside the explicit repository root, and
remain contained after symlink resolution; an artifact names an exact retained
file. URL references use HTTP(S) with a hostname. Command references are inert
strings and cannot establish evidence by themselves; use retained output or
another supporting source. Never execute a reference just to validate it.

Ordinary statuses are `draft`, `current`, and `superseded`; superseded pages name
an existing local/artifact replacement in `superseded_by`. Use the
[Documentation and ADRs method](../documentation-and-adrs/SKILL.md) for ADR
statuses, human decision evidence, and preserved history.

Templates retain required field shapes and use explicit `<...>` placeholders
for values to replace. Only configured template paths receive placeholder date
and reference-existence exemptions; nonplaceholder references still resolve.
Configured example pages require `example: true`, complete real metadata, and
an explicit illustrative notice. Examples are not evidence of project decisions.
Indexes, navigation pages, logs, raw inputs, companions, templates, and examples
are classified by explicit configuration, never by a guessed filename.

## Write, log, then check

After approved edits, maintain affected topic metadata, descriptions, hints,
indexes, links, and the configured action log. Its machine-readable entries use
the format in the [example log](../../knowledge/log.md); adapt the approved log
path, never copy fabricated events. Record actual timestamps, actions, evidence,
and check results. A prior check cannot certify a later log write.

Run the configured integrity check **after the final knowledge write**, including
navigation and log edits. Map applicable checks to a compatible existing target
checker, translated checks, or the optional portable
[validator](../../scripts/validate_knowledge.py). That reference implementation
requires Python 3.10+ standard library only and an explicit target classification
layout; the [example layout](../../knowledge/validation-layout.yaml) is illustrative.
Its bounded YAML input forms, typed parse errors, and resource limits are documented
in the [checker guide](../../knowledge/README.md#supported-input-forms); these limits
do not narrow the portable metadata contract or a compatible target checker.
It checks metadata, local links and supported anchors, hints, ADR structure, and log
integrity, rejects duplicate keys, and never executes reference commands or checks
remote availability. Reasoning must still assess truth, relevance, contradictions,
and human evidence.
Required checks that fail or cannot run block retention. If no checks apply,
record the reason explicitly rather than treating an unavailable check as absent.

For a target adapter, include or translate the required knowledge contract into
approved native paths and inventory included, translated, referenced, and omitted
linked assets with reasons. Example log/layout files need not be copied. Selecting
the reference checker requires mapping its runtime, actual target classifications,
and check command; other adoptions do not require Python. Its maintainer tests are
not automatically created, run, or copied into targets. Rewrite or remove projected
links and commands consistently; do not copy the example tree wholesale.

## Report

Return the authoritative [Knowledge Outcome](../../schemas/artifacts.md#knowledge-outcome)
with `applicable`, `status`, mandatory `reason`, `evidence`, `files_changed`,
`checks`, and `remaining_work`. `updated` requires eligible completed writes and
passed applicable checks after final writes; `no_change` requires an actual
assessment finding no eligible learning. Missing approved paths, ambiguous policy,
failed writes, unavailable required checks, and failed checks are `blocked`, with
completed partial writes and remaining work distinguished. `outside_scope` applies
only to partial adoption excluding knowledge management. Empty writes do not
prove assessment, and this source repository's example tree is never a default
home for run-specific learning.
